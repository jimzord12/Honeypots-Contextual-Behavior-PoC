package db

import "gorm.io/gorm"

func CreateTables(db *gorm.DB) {
	db.AutoMigrate(&Attack{})
}
