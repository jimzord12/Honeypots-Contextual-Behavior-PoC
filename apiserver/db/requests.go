package db

// AttackRequest represents the expected JSON payload for creating an attack
type AttackRequest struct {
	Type uint `json:"type" binding:"required"` // Using string to map to AttackType
	// SessionID   uint              `json:"session_id" binding:"required"`
	// Timestamp   time.Time         `json:"timestamp" binding:"required"`
	SourceIP    string         `json:"source_ip" binding:"required,ip"`
	DestIP      string         `json:"dest_ip" binding:"required,ip"`
	Protocol    string         `json:"protocol" binding:"required"`
	Payload     map[string]any `json:"payload" binding:"required"`
	HttpHeaders map[string]any `json:"http_headers" binding:"required"`
	Path        string         `json:"path" binding:"required"`
}
