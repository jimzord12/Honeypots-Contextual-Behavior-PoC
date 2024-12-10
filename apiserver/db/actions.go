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

func ResetDatabase() error {
	// List of all tables to clear
	db = database.DbInstance.Db
	tables := []string{"attacks"} // Replace with your table names

	for _, table := range tables {
		if err := db.Exec("DELETE FROM " + table).Error; err != nil {
			log.Printf("Failed to clear table %s: %v", table, err)
			return err
		}
		log.Printf("Cleared table: %s", table)
	}

	log.Println("Database reset completed successfully.")
	return nil
}
