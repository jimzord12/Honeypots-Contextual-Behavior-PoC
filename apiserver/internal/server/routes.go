package server

import (
	"apiserver/db"
	"encoding/json"
	"log"
	"net/http"
)

func (s *Server) RegisterRoutes() http.Handler {

	mux := http.NewServeMux()
	mux.HandleFunc("/", s.HelloWorldHandler)
	mux.HandleFunc("/health", s.healthHandler)
	mux.HandleFunc("/create-attack", s.addAttack)

	return mux
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
	log.Printf("Incoming request: %v", r)

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
		http.Error(w, "Bad request: "+err.Error(), http.StatusBadRequest)
		return
	}

	if req.Type > 5 {
		http.Error(w, "Invalid attack type", http.StatusBadRequest)
		return
	}

	// Marshal Payload and HttpHeaders to JSON
	payloadJSON, err := json.Marshal(req.Payload)
	if err != nil {
		http.Error(w, "Invalid payload: "+err.Error(), http.StatusBadRequest)
		return
	}

	headersJSON, err := json.Marshal(req.HttpHeaders)
	if err != nil {
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

}
