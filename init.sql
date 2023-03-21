CREATE DATABASE regain;
USE regain;

/* 各種テーブル定義の作成 */
CREATE TABLE process_statuses(
    status_id INT AUTO_INCREMENT,
    status_name VARCHAR(10) NOT NULL,
    PRIMARY KEY (status_id),
    INDEX (status_id)
) ENGINE = InnoDB;

CREATE TABLE task_statuses(
    status_id INT AUTO_INCREMENT,
    status_name VARCHAR(10) NOT NULL,
    PRIMARY KEY (status_id),
    INDEX (status_id)
) ENGINE = InnoDB;

CREATE TABLE priorities(
    priority_id INT AUTO_INCREMENT,
    priority_name VARCHAR(10) NOT NULL,
    PRIMARY KEY (priority_id),
    INDEX (priority_id)
) ENGINE = InnoDB;

CREATE TABLE projects(
    project_id INT AUTO_INCREMENT,
    project_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (project_id),
    INDEX (project_id)
) ENGINE = InnoDB;

CREATE TABLE processes(
    process_id INT AUTO_INCREMENT,
    process_name VARCHAR(20) NOT NULL,
    status_id INT NOT NULL DEFAULT 1,
    project_id INT NOT NULL,
    deadline DATE NOT NULL,
    PRIMARY KEY (process_id),
    FOREIGN KEY (status_id) REFERENCES process_statuses(status_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX (process_id)
) ENGINE = InnoDB;

CREATE TABLE tasks(
    task_id INT AUTO_INCREMENT,
    task_name VARCHAR(255) NOT NULL,
    status_id INT NOT NULL DEFAULT 1,
    process_id INT NOT NULL,
    priority_id INT NOT NULL DEFAULT 1,
    estimated_time TIME NOT NULL DEFAULT "0:00:00",
    deadline DATE NOT NULL,
    PRIMARY KEY (task_id),
    FOREIGN KEY (status_id) REFERENCES task_statuses(status_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (process_id) REFERENCES processes(process_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (priority_id) REFERENCES priorities(priority_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX (task_id)
) ENGINE = InnoDB;

CREATE TABLE commits(
    commit_id INT AUTO_INCREMENT,
    task_id INT NOT NULL,
    commit_date DATE NOT NULL,
    commit_time TIME NOT NULL,
    PRIMARY KEY (commit_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX (commit_id),
    UNIQUE unique_task_id_cammit_date_index (task_id, commit_date)
) ENGINE = InnoDB;

GRANT SELECT, UPDATE, INSERT, DELETE ON regain.* TO "regain_app" IDENTIFIED BY "regain_app";

/* パラメータデータの投入(仮) */
INSERT INTO process_statuses(
    status_name
) VALUES ("未着手"), ("着手"), ("完了");

INSERT INTO task_statuses(
    status_name
) VALUES ("未着手"), ("着手"), ("完了");

INSERT INTO priorities(
    priority_name
) VALUES ("最低"), ("低"), ("中"), ("高"), ("最高");

/* 試験用初期データの投入 */
INSERT INTO projects(
    project_name
) VALUES ("顧客情報管理システム"), ("BigData分析"), ("プロジェクトC");

INSERT INTO processes(
    process_name, project_id, deadline
) VALUES (
    "要件定義", 1, "2023-03-01"
), (
    "基本設計", 1, "2023-03-30"
), (
    "詳細設計", 1, "2023-03-30"
), (
    "開発", 1, "2023-04-28"
), (
    "データ取得", 2, "2023-02-18"
), (
    "データ分析", 2, "2023-04-18"
), (
    "データ報告", 2, "2023-04-28"
), (
    "工程A", 3, "2023-03-22"
), (
    "工程B", 3, "2023-03-23"
), (
    "工程C", 3, "2023-03-24"
);

INSERT INTO tasks(
    task_name, process_id, deadline
) VALUES (
    "システム概要記述", 1, "2023-02-21"
), (
    "開発目的記述", 1, "2023-02-28"
), (
    "拡張性記述", 2, "2023-03-10"
), (
    "耐障害性記述", 2, "2023-03-17"
), (
    "ほげほげ記述", 2, "2023-03-27"
);

INSERT INTO commits(
    task_id, commit_date, commit_time
) VALUES (
    1, "2023-02-15", "1:05:00"
), (
    1, "2023-02-21", "1:22:00"
), (
    2, "2023-02-24", "1:30:00"
), (
    2, "2023-02-27", "1:22:00"
), (
    3, "2023-03-02", "0:37:00"
), (
    3, "2023-03-09", "4:34:00"
), (
    4, "2023-03-14", "0:45:00"
);
