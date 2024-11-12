package db

import (
	"time"

	"gorm.io/datatypes"
	"gorm.io/gorm"
)

type AttackType int

const (
	SQL_Injection = iota + 1
	XSS_Attack
	Dos
	PortScanning
	BruteForceLogin
)

// Attack represents an attack record
type Attack struct {
	gorm.Model
	Type AttackType `gorm:"type:integer;not null"`
	// SessionID   uint           `gorm:"not null;index"` // Foreign key
	Timestamp   time.Time      `gorm:"not null"`
	SourceIP    string         `gorm:"size:45"` // Supports IPv6
	DestIP      string         `gorm:"size:45"`
	Protocol    string         `gorm:"size:10"`
	Payload     datatypes.JSON `gorm:"type:TEXT"` // Store JSON as TEXT
	HttpHeaders datatypes.JSON `gorm:"type:TEXT"` // Store JSON as TEXT
	Path        string         `gorm:"size:120"`
}

// Session represents a session record
// type Session struct {
// 	gorm.Model
// 	Duration time.Duration
// 	Attempts int
// 	Attacks  []Attack `gorm:"foreignKey:SessionID"` // One-to-Many relationship
// }

func NewAttack(atkType AttackType, sourceIp string, destIp string, protocol string, payload datatypes.JSON, httpHeaders datatypes.JSON, path string) *Attack {
	return &Attack{
		Type: atkType,
		// SessionID:   sessionID,
		Timestamp:   time.Now(),
		SourceIP:    sourceIp,
		DestIP:      destIp,
		Protocol:    protocol,
		Payload:     payload,
		HttpHeaders: httpHeaders,
		Path:        path,
	}
}

// func NewSession(duration time.Duration, attempts int) *Session {
// 	return &Session{
// 		Duration: duration,
// 		Attempts: attempts,
// 	}
// }
