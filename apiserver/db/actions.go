package db

import (
	"apiserver/internal/database"
	"errors"
	"log"

	"gorm.io/gorm"
)

var db *gorm.DB

func CreateAttack_DB(atk *Attack) error {
	db = database.DbInstance.Db
	if db == nil {
		return errors.New("database connection is nil")
	}

	if res := db.Create(atk); res.Error != nil {
		return res.Error
	}

	log.Printf("createAttack_DB: Attack record created successfully")
	log.Printf("\n\nThe attack record: %+v", atk)
	return nil
}
