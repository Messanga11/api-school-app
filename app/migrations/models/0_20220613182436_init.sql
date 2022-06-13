-- upgrade --
CREATE TABLE IF NOT EXISTS `conversation` (
    `uuid` CHAR(36) NOT NULL  PRIMARY KEY
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `guardian` (
    `uuid` CHAR(36) NOT NULL  PRIMARY KEY,
    `phone_number` VARCHAR(9) NOT NULL UNIQUE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `school` (
    `uuid` CHAR(36) NOT NULL  PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `region` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `password` VARCHAR(100) NOT NULL,
    `type` VARCHAR(100) NOT NULL  DEFAULT 'SCHOOL',
    `principal` JSON,
    `vice_principals` JSON,
    `logo` LONGTEXT,
    `teachers` JSON
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `schoolpost` (
    `uuid` CHAR(36) NOT NULL  PRIMARY KEY,
    `title` VARCHAR(200) NOT NULL,
    `description` LONGTEXT NOT NULL,
    `image_url` VARCHAR(100),
    `base_64` LONGTEXT,
    `school_id` CHAR(36) NOT NULL,
    CONSTRAINT `fk_schoolpo_school_61039213` FOREIGN KEY (`school_id`) REFERENCES `school` (`uuid`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `subject` (
    `uuid` CHAR(36) NOT NULL  PRIMARY KEY,
    `title` VARCHAR(200) NOT NULL,
    `visible_for` VARCHAR(3) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `paper` (
    `uuid` CHAR(36) NOT NULL  PRIMARY KEY,
    `year` INT NOT NULL,
    `paper_type` VARCHAR(200) NOT NULL,
    `visible_for` VARCHAR(3) NOT NULL,
    `subject_id` CHAR(36) NOT NULL,
    CONSTRAINT `fk_paper_subject_ad5069dd` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`uuid`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `question` (
    `uuid` CHAR(36) NOT NULL  PRIMARY KEY,
    `is_an_image` BOOL NOT NULL  DEFAULT 0,
    `image` LONGTEXT NOT NULL,
    `text` VARCHAR(100) NOT NULL,
    `paper_id` CHAR(36) NOT NULL,
    CONSTRAINT `fk_question_paper_24845dc8` FOREIGN KEY (`paper_id`) REFERENCES `paper` (`uuid`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `answer` (
    `uuid` CHAR(36) NOT NULL  PRIMARY KEY,
    `is_an_image` BOOL NOT NULL  DEFAULT 0,
    `image` LONGTEXT NOT NULL,
    `text` VARCHAR(100) NOT NULL,
    `letter` VARCHAR(3) NOT NULL,
    `is_correct` BOOL NOT NULL  DEFAULT 0,
    `question_id` CHAR(36) NOT NULL,
    CONSTRAINT `fk_answer_question_a50dccbd` FOREIGN KEY (`question_id`) REFERENCES `question` (`uuid`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `topic` (
    `uuid` CHAR(36) NOT NULL  PRIMARY KEY,
    `title` VARCHAR(100) NOT NULL,
    `subject_uuid` VARCHAR(100) NOT NULL,
    `visible_for` VARCHAR(3) NOT NULL,
    `subject_id` CHAR(36) NOT NULL,
    CONSTRAINT `fk_topic_subject_d8b0a419` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`uuid`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `book` (
    `uuid` CHAR(36) NOT NULL  PRIMARY KEY,
    `title` VARCHAR(100) NOT NULL,
    `url` VARCHAR(100) NOT NULL,
    `topic_id` CHAR(36) NOT NULL,
    CONSTRAINT `fk_book_topic_179834a8` FOREIGN KEY (`topic_id`) REFERENCES `topic` (`uuid`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `filemodel` (
    `uuid` CHAR(36) NOT NULL  PRIMARY KEY,
    `title` VARCHAR(120) NOT NULL,
    `url` VARCHAR(100) NOT NULL,
    `type` VARCHAR(9) NOT NULL,
    `topic_id` CHAR(36),
    CONSTRAINT `fk_filemode_topic_a411455a` FOREIGN KEY (`topic_id`) REFERENCES `topic` (`uuid`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `note` (
    `uuid` CHAR(36) NOT NULL  PRIMARY KEY,
    `url` VARCHAR(100) NOT NULL,
    `topic_id` CHAR(36) NOT NULL,
    CONSTRAINT `fk_note_topic_a24ab7f5` FOREIGN KEY (`topic_id`) REFERENCES `topic` (`uuid`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `pdf` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `uuid` CHAR(36) NOT NULL,
    `title_id` CHAR(36) NOT NULL,
    CONSTRAINT `fk_pdf_topic_27af83dc` FOREIGN KEY (`title_id`) REFERENCES `topic` (`uuid`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `uuid` CHAR(36) NOT NULL  PRIMARY KEY,
    `first_name` VARCHAR(100) NOT NULL,
    `last_name` VARCHAR(100) NOT NULL,
    `user_name` VARCHAR(20) NOT NULL UNIQUE,
    `email` VARCHAR(200) NOT NULL UNIQUE,
    `image_url` VARCHAR(100)  UNIQUE,
    `phone_number` VARCHAR(9) NOT NULL,
    `gender` VARCHAR(6) NOT NULL,
    `exam` VARCHAR(30) NOT NULL,
    `selected_exam` JSON NOT NULL,
    `guardian_phone_number` VARCHAR(9) NOT NULL,
    `password` VARCHAR(100) NOT NULL,
    `is_verified` BOOL NOT NULL  DEFAULT 0,
    `role` VARCHAR(10) NOT NULL,
    `join_date` DATETIME(6) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `friendmatch` (
    `uuid` CHAR(36) NOT NULL  PRIMARY KEY,
    `main_user_uuid` VARCHAR(100) NOT NULL,
    `accepted` BOOL NOT NULL  DEFAULT 0,
    `request_user_id` CHAR(36) NOT NULL,
    CONSTRAINT `fk_friendma_user_4584799d` FOREIGN KEY (`request_user_id`) REFERENCES `user` (`uuid`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `message` (
    `uuid` CHAR(36) NOT NULL  PRIMARY KEY,
    `text` LONGTEXT NOT NULL,
    `unread` BOOL NOT NULL  DEFAULT 0,
    `sender_uuid` VARCHAR(100) NOT NULL,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `conversation_id` CHAR(36) NOT NULL,
    `receiver_id` CHAR(36),
    `receiver_guardian_id` CHAR(36),
    CONSTRAINT `fk_message_conversa_b406696e` FOREIGN KEY (`conversation_id`) REFERENCES `conversation` (`uuid`) ON DELETE CASCADE,
    CONSTRAINT `fk_message_user_9422999f` FOREIGN KEY (`receiver_id`) REFERENCES `user` (`uuid`) ON DELETE CASCADE,
    CONSTRAINT `fk_message_guardian_afe15a70` FOREIGN KEY (`receiver_guardian_id`) REFERENCES `guardian` (`uuid`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `video` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `uuid` VARCHAR(100) NOT NULL UNIQUE DEFAULT '5d845658-8fc6-4169-aafc-f4c652871179',
    `title` VARCHAR(100) NOT NULL,
    `url` VARCHAR(100) NOT NULL,
    `topic_uuid` VARCHAR(100) NOT NULL,
    `topic_id` INT NOT NULL,
    CONSTRAINT `fk_video_video_04c986f3` FOREIGN KEY (`topic_id`) REFERENCES `video` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user_conversation` (
    `conversation_id` CHAR(36) NOT NULL,
    `user_id` CHAR(36) NOT NULL,
    FOREIGN KEY (`conversation_id`) REFERENCES `conversation` (`uuid`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `user` (`uuid`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
