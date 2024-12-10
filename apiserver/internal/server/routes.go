package server

import (
	"apiserver/db"
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

func (s *Server) RegisterRoutes() http.Handler {

	mux := http.NewServeMux()
	mux.HandleFunc("/", s.HelloWorldHandler)
	mux.HandleFunc("/health", s.healthHandler)
	mux.HandleFunc("/create-attack", s.addAttack)
	mux.HandleFunc("/reset-db", s.resetDatabaseHandler)

	// Wrap the mux with a custom NotFound handler
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if _, pattern := mux.Handler(r); pattern == "" {
			s.notFound(w, r)
			return
		}
		mux.ServeHTTP(w, r)
	})
}

func (s *Server) resetDatabaseHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Call the ResetDatabase function
	err := db.ResetDatabase()
	if err != nil {
		http.Error(w, "Failed to reset the database", http.StatusInternalServerError)
		log.Printf("Database reset error: %v", err)
		return
	}

	// Respond with success
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	response := map[string]string{
		"message": "Database reset successfully",
	}
	json.NewEncoder(w).Encode(response)
}

func (s *Server) notFound(w http.ResponseWriter, r *http.Request) {
	resp := map[string]string{
		"message": "Resource not found",
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusNotFound)

	jsonResp, err := json.Marshal(resp)
	if err != nil {
		log.Printf("Failed to marshal JSON in notFound handler: %v", err)
		http.Error(w, "Internal server error", http.StatusInternalServerError)
		return
	}

	_, err = w.Write(jsonResp)
	if err != nil {
		log.Printf("Failed to write response in notFound handler: %v", err)
	}
}

func (s *Server) HelloWorldHandler(w http.ResponseWriter, r *http.Request) {
	resp := make(map[string]string)
	resp["message"] = "Hello World"

	jsonResp, err := json.Marshal(resp)
	if err != nil {
		log.Fatalf("error handling JSON marshal. Err: %v", err)
	}

	_, _ = w.Write(jsonResp)
}

func (s *Server) healthHandler(w http.ResponseWriter, r *http.Request) {
	jsonResp, err := json.Marshal(s.db.Health())

	if err != nil {
		log.Fatalf("error handling JSON marshal. Err: %v", err)
	}

	_, _ = w.Write(jsonResp)
}

func (s *Server) addAttack(w http.ResponseWriter, r *http.Request) {
	log.Printf("Incoming request: %+v", r)

	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// The request will be coming in as JSON
	// Parse the JSON and create an Attack object
	// Call the db package to create the Attack record
	// Return a response to the client

	var req db.AttackRequest
	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields() // Prevent unknown fields

	if err := decoder.Decode(&req); err != nil {
		fmt.Print("Problem Decoding the Request's Body")
		http.Error(w, "Bad request: "+err.Error(), http.StatusBadRequest)
		return
	}

	if req.Type > 5 {
		http.Error(w, "Invalid attack type", http.StatusBadRequest)
		return
	}

	// Marshal Payload and HttpHeaders to JSON
	payloadJSON, err := json.Marshal(req.Payload)
	fmt.Printf("REQUEST Payload: %+v", req.Payload)
	if err != nil {
		http.Error(w, "Invalid payload: "+err.Error(), http.StatusBadRequest)
		return
	}

	headersJSON, err := json.Marshal(req.HttpHeaders)
	if err != nil {
		fmt.Printf("REQUEST HEADERS: %+v", req.HttpHeaders)
		http.Error(w, "Invalid HTTP headers: "+err.Error(), http.StatusBadRequest)
		return
	}

	// Create the Attack record
	attack := db.NewAttack(db.AttackType(req.Type), req.SourceIP, req.DestIP, req.Protocol, payloadJSON, headersJSON, req.Path)

	// Call the db package to create the Attack record
	err = db.CreateAttack_DB(attack)
	if err != nil {
		http.Error(w, "Internal server error", http.StatusInternalServerError)
		log.Printf("Error creating attack record: %v", err)
		return
	}

	// Respond with success
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	response := map[string]any{
		"message": "Attack record created successfully",
		"id":      attack.ID,
	}
	json.NewEncoder(w).Encode(response)

	// Send the attack to the FastAPI server for further processing
	go forwardToMLModel(*attack)

}

// forwardToMLModel sends the attack data to the FastAPI server
func forwardToMLModel(attack db.Attack) {
	// Define the FastAPI endpoint URL
	fastAPIURL := "http://localhost:8000/process-attack"

	// Prepare the attack data as JSON
	attackData := map[string]interface{}{
		"id":           attack.ID,
		"type":         attack.Type,
		"timestamp":    attack.Timestamp,
		"source_ip":    attack.SourceIP,
		"dest_ip":      attack.DestIP,
		"protocol":     attack.Protocol,
		"payload":      json.RawMessage(attack.Payload),
		"http_headers": json.RawMessage(attack.HttpHeaders),
		"path":         attack.Path,
		"skill_score":  attack.SkillScore,
		"skill_level":  attack.SkillLevel,
	}

	// Convert attack data to JSON
	jsonData, err := json.Marshal(attackData)
	if err != nil {
		log.Printf("Failed to marshal attack data: %v", err)
		return
	}

	// Send the JSON data to the FastAPI server
	resp, err := http.Post(fastAPIURL, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		log.Printf("Failed to send attack data to FastAPI server: %v", err)
		return
	}
	defer resp.Body.Close()

	// Log the response from the FastAPI server
	if resp.StatusCode == http.StatusOK {
		log.Print("Attack data successfully sent to FastAPI server")
	} else {
		log.Printf("FastAPI server returned status %d", resp.StatusCode)
	}
}
