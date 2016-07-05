package main

import (
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
	//"github.com/go-xorm/xorm"
	"github.com/Unknwon/goconfig"
	_ "gopkg.in/rana/ora.v3"
	"log"
	"os"
)

func main() {
	log.Println("TOM同步")

	log.Println("开始加载配置文件")
	cfg, err := goconfig.LoadConfigFile("sync.ini")
	if err != nil {
		panic(err)
	}
	log.Println("配置文件加载完成，开始尝试连接源数据库和目标数据库")

	db_type, err := cfg.GetValue("db1", "type")
	db_host, err := cfg.GetValue("db1", "host")
	db_port, err := cfg.GetValue("db1", "port")
	db_user, err := cfg.GetValue("db1", "user")
	db_pass, err := cfg.GetValue("db1", "pass")
	db_name, err := cfg.GetValue("db1", "name")

	// 连接 Oracle 源数据库
	db1, err := sql.Open(db_type, db_user+"/"+db_pass+"@"+db_host+":"+db_port+"/"+db_name)
	if err != nil {
		log.Println("无法正确连接到Oracle源数据库")
		panic(err)
	}
	defer db1.Close()

	db_type, err = cfg.GetValue("db2", "type")
	db_host, err = cfg.GetValue("db2", "host")
	db_port, err = cfg.GetValue("db2", "port")
	db_user, err = cfg.GetValue("db2", "user")
	db_pass, err = cfg.GetValue("db2", "pass")
	db_name, err = cfg.GetValue("db2", "name")

	// 连接目标 MySQL 数据库
	os.Setenv("PKG_CONFIG_PATH", "~/Library/pkg_config") // 找到oci8.pc
	db2, err := sql.Open(db_type, db_user+":"+db_pass+"@tcp("+db_host+":"+db_port+")/"+db_name)
	if err != nil {
		log.Println("无法正确连接到MySQL目标数据库")
		panic(err)
	}
	defer db2.Close()

	log.Println("正确连接到数据库，现在开始同步数据...")

	// 连接测试
	rows, err := db1.Query("SELECT * FROM TABLE LIMIT ?, 50", 0)
	if err != nil {
		panic(err)
	}
	for rows.Next() {
		var f1 float32
		var f2 string
		rows.Scan(&f1, &f2)
		log.Println(f1, f2)
	}
}
