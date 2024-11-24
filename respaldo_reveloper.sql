-- MySQL dump 10.13  Distrib 8.2.0, for Win64 (x86_64)
--
-- Host: localhost    Database: reveloper
-- ------------------------------------------------------
-- Server version	8.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (2,'Administrador'),(1,'Desarrollador');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (2,1,24),(4,1,28),(3,1,32),(1,1,40),(5,2,1),(6,2,2),(7,2,3),(8,2,4),(9,2,5),(10,2,6),(11,2,7),(12,2,8),(13,2,9),(14,2,10),(15,2,11),(16,2,12),(17,2,13),(18,2,14),(19,2,15),(20,2,16),(21,2,17),(22,2,18),(23,2,19),(24,2,20),(25,2,21),(26,2,22),(27,2,23),(28,2,24),(29,2,25),(30,2,26),(31,2,27),(32,2,28),(33,2,29),(34,2,30),(35,2,31),(36,2,32),(37,2,33),(38,2,34),(39,2,35),(40,2,36),(41,2,37),(42,2,38),(43,2,39),(44,2,40);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add proyecto',6,'add_proyecto'),(22,'Can change proyecto',6,'change_proyecto'),(23,'Can delete proyecto',6,'delete_proyecto'),(24,'Can view proyecto',6,'view_proyecto'),(25,'Can add tarea por desarrollar',7,'add_tareapordesarrollar'),(26,'Can change tarea por desarrollar',7,'change_tareapordesarrollar'),(27,'Can delete tarea por desarrollar',7,'delete_tareapordesarrollar'),(28,'Can view tarea por desarrollar',7,'view_tareapordesarrollar'),(29,'Can add tarea desarrollada',8,'add_tareadesarrollada'),(30,'Can change tarea desarrollada',8,'change_tareadesarrollada'),(31,'Can delete tarea desarrollada',8,'delete_tareadesarrollada'),(32,'Can view tarea desarrollada',8,'view_tareadesarrollada'),(33,'Can add user',9,'add_usuario'),(34,'Can change user',9,'change_usuario'),(35,'Can delete user',9,'delete_usuario'),(36,'Can view user',9,'view_usuario'),(37,'Can add evaluacion',10,'add_evaluacion'),(38,'Can change evaluacion',10,'change_evaluacion'),(39,'Can delete evaluacion',10,'delete_evaluacion'),(40,'Can view evaluacion',10,'view_evaluacion'),(41,'Can add Tarea Completada',11,'add_tareascompletadas'),(42,'Can change Tarea Completada',11,'change_tareascompletadas'),(43,'Can delete Tarea Completada',11,'delete_tareascompletadas'),(44,'Can view Tarea Completada',11,'view_tareascompletadas'),(45,'Can add evaluacion config',12,'add_evaluacionconfig'),(46,'Can change evaluacion config',12,'change_evaluacionconfig'),(47,'Can delete evaluacion config',12,'delete_evaluacionconfig'),(48,'Can view evaluacion config',12,'view_evaluacionconfig');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_Reveloper_usuario_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_Reveloper_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `reveloper_usuario` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2024-11-17 22:39:24.153589','1','admin',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Groups\", \"User permissions\"]}}]',9,1),(2,'2024-11-17 22:55:02.903283','2','Developer1',1,'[{\"added\": {}}]',9,1),(3,'2024-11-17 22:56:27.400626','2','Developer1',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Groups\"]}}]',9,1),(4,'2024-11-17 22:58:09.279673','PW1','Pagina_web1',1,'[{\"added\": {}}]',6,1),(5,'2024-11-17 23:00:05.448633','CCSSPW1','Crear CSS Página web 1',1,'[{\"added\": {}}]',7,1),(6,'2024-11-17 23:03:04.353559','1','Evaluación CSS PW1',1,'[{\"added\": {}}]',10,1),(7,'2024-11-18 18:10:45.780853','3','Developer2',1,'[{\"added\": {}}]',9,1),(8,'2024-11-18 18:11:26.666352','3','Developer2',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Groups\"]}}]',9,1),(9,'2024-11-18 18:12:29.051755','EC1','Ecommerce1',1,'[{\"added\": {}}]',6,1),(10,'2024-11-18 18:14:57.287819','LEC1','Login Ecommerce1',1,'[{\"added\": {}}]',7,1),(11,'2024-11-18 18:17:08.189917','2','Evaluación LEC1',1,'[{\"added\": {}}]',10,1),(12,'2024-11-18 18:22:40.577685','HTMLPW1','Crear la plantilla HTML',1,'[{\"added\": {}}]',7,1),(13,'2024-11-18 18:24:03.807155','3','Evaluación HTMLPW1',1,'[{\"added\": {}}]',10,1),(14,'2024-11-18 18:30:31.197110','1','admin',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',9,1),(15,'2024-11-21 13:15:13.610702','4','Developer3',1,'[{\"added\": {}}]',9,1),(16,'2024-11-21 13:16:10.648201','4','Developer3',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Groups\"]}}]',9,1),(17,'2024-11-21 13:23:44.316910','ModPW1','Modal Pagina web 1',1,'[{\"added\": {}}]',7,1),(18,'2024-11-21 17:04:01.688569','4','Evaluación Modal PW1',1,'[{\"added\": {}}]',10,1),(19,'2024-11-22 13:21:12.390931','TP1','Tarea prueba 1',1,'[{\"added\": {}}]',7,1),(20,'2024-11-22 13:21:36.690587','TP1','Tarea prueba 1',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',7,1),(21,'2024-11-22 13:22:07.589311','TP1','Tarea prueba 1',2,'[]',7,1),(22,'2024-11-22 13:23:11.403840','TP1','Tarea prueba 1',2,'[]',7,1),(23,'2024-11-22 13:28:23.044875','TP1','Tarea prueba 1',2,'[]',7,1),(24,'2024-11-22 17:08:46.442104','P5','Sistema de recuperaciones',1,'[{\"added\": {}}]',6,1),(25,'2024-11-22 17:10:22.637716','T1','Analisis del problema',1,'[{\"added\": {}}]',7,1),(26,'2024-11-22 17:11:08.550544','T2','Diseño de base de datos',1,'[{\"added\": {}}]',7,1),(27,'2024-11-22 17:12:57.030018','T1','Analisis del problema',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',7,1),(28,'2024-11-22 21:23:40.093852','T2','Diseño de base de datos',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',7,1),(29,'2024-11-22 21:28:58.399488','2','Developer1',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',9,1),(30,'2024-11-23 13:29:51.669060','TP1','Tarea prueba 1',2,'[]',7,1),(31,'2024-11-23 13:31:38.982311','HTMLPW1','Crear la plantilla HTML',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',7,1),(32,'2024-11-23 13:48:19.001087','TP3','tarea prueba 3',1,'[{\"added\": {}}]',7,1),(33,'2024-11-23 14:25:12.071830','TP3','tarea prueba 3',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',7,1),(34,'2024-11-23 14:25:34.131426','ModPW1','Modal Pagina web 1',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',7,1),(35,'2024-11-23 14:25:42.030783','LEC1','Login Ecommerce1',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',7,1),(36,'2024-11-23 14:26:00.663702','CCSSPW1','Crear CSS Página web 1',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',7,1),(37,'2024-11-24 14:46:15.155926','5','Evaluación de Tarea de Prueba',2,'[{\"changed\": {\"fields\": [\"Calificacion\"]}}]',10,1),(38,'2024-11-24 18:10:56.082576','OLSR1','Funcionalidad obtener liquidaciones',1,'[{\"added\": {}}]',7,1),(39,'2024-11-24 18:51:19.738945','1','Configuración de Evaluación',1,'[{\"added\": {}}]',12,1),(40,'2024-11-24 18:54:18.833701','ISSR1','Funcionalidad informes sociales Salud',1,'[{\"added\": {}}]',7,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(10,'Reveloper','evaluacion'),(12,'Reveloper','evaluacionconfig'),(6,'Reveloper','proyecto'),(8,'Reveloper','tareadesarrollada'),(7,'Reveloper','tareapordesarrollar'),(11,'Reveloper','tareascompletadas'),(9,'Reveloper','usuario'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-11-08 16:35:25.510193'),(2,'contenttypes','0002_remove_content_type_name','2024-11-08 16:35:25.652316'),(3,'auth','0001_initial','2024-11-08 16:35:26.158206'),(4,'auth','0002_alter_permission_name_max_length','2024-11-08 16:35:26.268365'),(5,'auth','0003_alter_user_email_max_length','2024-11-08 16:35:26.283973'),(6,'auth','0004_alter_user_username_opts','2024-11-08 16:35:26.294980'),(7,'auth','0005_alter_user_last_login_null','2024-11-08 16:35:26.302634'),(8,'auth','0006_require_contenttypes_0002','2024-11-08 16:35:26.302634'),(9,'auth','0007_alter_validators_add_error_messages','2024-11-08 16:35:26.315643'),(10,'auth','0008_alter_user_username_max_length','2024-11-08 16:35:26.347575'),(11,'auth','0009_alter_user_last_name_max_length','2024-11-08 16:35:26.347575'),(12,'auth','0010_alter_group_name_max_length','2024-11-08 16:35:26.364359'),(13,'auth','0011_update_proxy_permissions','2024-11-08 16:35:26.379457'),(14,'auth','0012_alter_user_first_name_max_length','2024-11-08 16:35:26.379457'),(19,'sessions','0001_initial','2024-11-08 16:35:27.963954'),(35,'Reveloper','0001_initial','2024-11-17 20:10:20.322783'),(36,'Reveloper','0002_remove_evaluacion_calificacion_and_more','2024-11-17 20:10:20.763909'),(37,'Reveloper','0003_evaluacion_calificacion_and_more','2024-11-17 20:10:20.813149'),(38,'Reveloper','0004_remove_evaluacion_estado_and_more','2024-11-17 20:10:20.857391'),(39,'Reveloper','0005_remove_evaluacion_fecha_vencimiento','2024-11-17 20:10:20.884402'),(40,'Reveloper','0006_remove_evaluacion_descripcion_evaluacion_comentarios','2024-11-17 20:10:21.012391'),(41,'Reveloper','0007_rename_fecha_creacion_evaluacion_fecha_evaluacion','2024-11-17 20:10:21.048047'),(42,'Reveloper','0008_evaluacion_tarea','2024-11-17 20:10:21.169808'),(43,'admin','0001_initial','2024-11-17 20:10:21.417846'),(44,'admin','0002_logentry_remove_auto_add','2024-11-17 20:10:21.426537'),(45,'admin','0003_logentry_add_action_flag_choices','2024-11-17 20:10:21.440201'),(46,'Reveloper','0009_delete_tareadesarrollada','2024-11-21 22:26:50.268665'),(47,'Reveloper','0010_alter_evaluacion_options_and_more','2024-11-22 13:15:00.867079'),(48,'Reveloper','0011_usuario_tareas_completadas','2024-11-22 21:20:23.546378'),(49,'Reveloper','0012_alter_tareapordesarrollar_estado','2024-11-24 14:14:17.379631'),(50,'Reveloper','0013_evaluacionconfig','2024-11-24 18:48:35.419922');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('zzkp1ke0ig8tr5lpnxfp2c4pubvkq39x','.eJxVjMEOwiAQRP-FsyFFugt49N5vIAuLUjWQlPZk_Hdp0oMeZ96beQtP25r91tLiZxYXocXptwsUn6nsgB9U7lXGWtZlDnJX5EGbnCqn1_Vw_w4ytdzXboxgA7uIYxpuGFCBBkJ0iq1GYDAa2VpjHJukzg7NoFOXCUIPiOLzBcalNrc:1tFI58:qAn52Vxf3tqZBqj9YW-xjcQdgua4EAEj-Lsbkg3up-s','2024-12-08 19:15:42.908683');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reveloper_evaluacion`
--

DROP TABLE IF EXISTS `reveloper_evaluacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reveloper_evaluacion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `proyecto_id` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `usuario_id` bigint NOT NULL,
  `fecha_evaluacion` datetime(6) NOT NULL,
  `titulo` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `calificacion` decimal(4,1) DEFAULT NULL,
  `comentarios` longtext COLLATE utf8mb4_general_ci NOT NULL DEFAULT (_utf8mb3'Comentario pendiente'),
  `tarea_id` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Reveloper_evaluacion_proyecto_id_e89e758b_fk_Reveloper` (`proyecto_id`),
  KEY `Reveloper_evaluacion_usuario_id_395158ba_fk_Reveloper_usuario_id` (`usuario_id`),
  KEY `Reveloper_evaluacion_tarea_id_f861ce6e_fk_Reveloper` (`tarea_id`),
  CONSTRAINT `Reveloper_evaluacion_proyecto_id_e89e758b_fk_Reveloper` FOREIGN KEY (`proyecto_id`) REFERENCES `reveloper_proyecto` (`id`),
  CONSTRAINT `Reveloper_evaluacion_tarea_id_f861ce6e_fk_Reveloper` FOREIGN KEY (`tarea_id`) REFERENCES `reveloper_tareapordesarrollar` (`id`),
  CONSTRAINT `Reveloper_evaluacion_usuario_id_395158ba_fk_Reveloper_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `reveloper_usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reveloper_evaluacion`
--

LOCK TABLES `reveloper_evaluacion` WRITE;
/*!40000 ALTER TABLE `reveloper_evaluacion` DISABLE KEYS */;
INSERT INTO `reveloper_evaluacion` VALUES (1,'PW1',2,'2024-11-17 23:01:00.000000','Evaluación CSS PW1',10.0,'¡Excelente CSS! ¡Roberto González es el mejor programador del mundo!','CCSSPW1'),(2,'EC1',3,'2024-11-18 18:16:15.000000','Evaluación LEC1',6.5,'Buen diseño de login.','LEC1'),(3,'PW1',2,'2024-11-18 18:23:07.000000','Evaluación HTMLPW1',9.5,'Muy buena plantilla HTML para la página web1.','HTMLPW1'),(4,'PW1',2,'2024-11-21 17:02:58.000000','Evaluación Modal PW1',8.9,'Evaluación del Modal para la página web1.','ModPW1'),(5,'EC1',2,'2024-11-24 14:45:34.000000','Evaluación de Tarea de Prueba',9.9,'Comentario pendiente','test001'),(6,'P5',2,'2024-11-24 18:07:33.706326','Evaluación de tarea prueba 3',NULL,'Comentario pendiente','TP3'),(7,'P5',4,'2024-11-24 18:16:14.672900','Evaluación de Funcionalidad obtener liquidaciones',NULL,'Comentario pendiente','OLSR1'),(8,'P5',4,'2024-11-24 18:56:38.355631','Evaluación de Funcionalidad informes sociales Salud',NULL,'Comentario pendiente','ISSR1'),(9,'EC1',3,'2024-11-24 19:12:20.500898','Evaluación para Login Ecommerce1',17.2,'Evaluación automática: Tiempo de Entrega: 10, Complejidad de la Tarea: 5.2, Número de Revisiones: 2','LEC1');
/*!40000 ALTER TABLE `reveloper_evaluacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reveloper_evaluacionconfig`
--

DROP TABLE IF EXISTS `reveloper_evaluacionconfig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reveloper_evaluacionconfig` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tiempo_entrega` decimal(4,1) NOT NULL,
  `complejidad_tarea` decimal(4,1) NOT NULL,
  `numero_revisiones` decimal(4,1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reveloper_evaluacionconfig`
--

LOCK TABLES `reveloper_evaluacionconfig` WRITE;
/*!40000 ALTER TABLE `reveloper_evaluacionconfig` DISABLE KEYS */;
INSERT INTO `reveloper_evaluacionconfig` VALUES (1,2.5,2.5,2.0);
/*!40000 ALTER TABLE `reveloper_evaluacionconfig` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reveloper_proyecto`
--

DROP TABLE IF EXISTS `reveloper_proyecto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reveloper_proyecto` (
  `id` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_general_ci,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `estado` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reveloper_proyecto`
--

LOCK TABLES `reveloper_proyecto` WRITE;
/*!40000 ALTER TABLE `reveloper_proyecto` DISABLE KEYS */;
INSERT INTO `reveloper_proyecto` VALUES ('EC1','Ecommerce1','Desarrollo de Ecommerce1.','2024-11-18','2024-11-30','activo'),('P5','Sistema de recuperaciones','Generar un sistema de recuperaciones para obtener liquidaciones, informes sociales correspondientes a salud e isapres','2024-11-22','2024-11-23','activo'),('PW1','Pagina_web1','Desarrollo de la primera página web.','2024-11-17','2024-11-30','activo');
/*!40000 ALTER TABLE `reveloper_proyecto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reveloper_tareapordesarrollar`
--

DROP TABLE IF EXISTS `reveloper_tareapordesarrollar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reveloper_tareapordesarrollar` (
  `id` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `titulo` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_general_ci,
  `fecha_creacion` datetime(6) NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `estado` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `proyecto_id` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `usuario_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Reveloper_tareaporde_usuario_id_d71d91df_fk_Reveloper` (`usuario_id`),
  KEY `Reveloper_tareaporde_proyecto_id_3a104c90_fk_Reveloper` (`proyecto_id`),
  CONSTRAINT `Reveloper_tareaporde_proyecto_id_3a104c90_fk_Reveloper` FOREIGN KEY (`proyecto_id`) REFERENCES `reveloper_proyecto` (`id`),
  CONSTRAINT `Reveloper_tareaporde_usuario_id_d71d91df_fk_Reveloper` FOREIGN KEY (`usuario_id`) REFERENCES `reveloper_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reveloper_tareapordesarrollar`
--

LOCK TABLES `reveloper_tareapordesarrollar` WRITE;
/*!40000 ALTER TABLE `reveloper_tareapordesarrollar` DISABLE KEYS */;
INSERT INTO `reveloper_tareapordesarrollar` VALUES ('','Nueva Tarea Pendiente','Descripción de la tarea pendiente','2024-11-23 14:19:52.895314','2024-12-01','pendiente','EC1',2),('CCSSPW1','Crear CSS Página web 1','Creación del CSS de la primera página web.','2024-11-17 23:00:05.448633','2024-11-30','pendiente','PW1',2),('HTMLPW1','Crear la plantilla HTML','Desarrollo de la plantilla HTML para la página web1.','2024-11-18 18:22:40.577685','2024-11-30','completada','PW1',2),('ISSR1','Funcionalidad informes sociales Salud','Funcionalidad informes sociales Salud del Sistema de recuperaciones.','2024-11-24 18:54:18.833701','2024-11-27','completada','P5',4),('LEC1','Login Ecommerce1','Desarrollo de login para ecommerce1','2024-11-18 18:14:57.276806','2024-11-30','completada','EC1',3),('ModPW1','Modal Pagina web 1','Desarrollo de un modal para la lista de usuarios en página web 1.','2024-11-21 13:23:44.316910','2024-11-30','pendiente','PW1',2),('OLSR1','Funcionalidad obtener liquidaciones','Funcionalidad obtener liquidaciones para el sistema de recuperaciones.','2024-11-24 18:10:56.080587','2024-11-30','completada','P5',4),('T1','Analisis del problema','Esta es una descripcion.','2024-11-22 17:10:22.637716','2024-11-23','completada','P5',2),('T2','Diseño de base de datos','Definicion de entidades y estructuras.','2024-11-22 17:11:08.537023','2024-11-23','completada','P5',2),('test001','Tarea de Prueba','Descripción de prueba','2024-11-24 14:28:25.758484','2024-11-24','completada','EC1',2),('TP1','Tarea prueba 1','Esta es una tarea de prueba.','2024-11-22 13:21:12.390931','2024-11-22','completada','EC1',3),('TP3','tarea prueba 3','tarea de prueba 3.','2024-11-23 13:48:19.001087','2024-11-30','completada','P5',2);
/*!40000 ALTER TABLE `reveloper_tareapordesarrollar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reveloper_tareascompletadas`
--

DROP TABLE IF EXISTS `reveloper_tareascompletadas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reveloper_tareascompletadas` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tarea_original_id` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `titulo` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `fecha_entrega` datetime(6) NOT NULL,
  `estado` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `comentario` longtext COLLATE utf8mb4_general_ci,
  `usuario_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Reveloper_tareascomp_usuario_id_9b745535_fk_Reveloper` (`usuario_id`),
  CONSTRAINT `Reveloper_tareascomp_usuario_id_9b745535_fk_Reveloper` FOREIGN KEY (`usuario_id`) REFERENCES `reveloper_usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reveloper_tareascompletadas`
--

LOCK TABLES `reveloper_tareascompletadas` WRITE;
/*!40000 ALTER TABLE `reveloper_tareascompletadas` DISABLE KEYS */;
INSERT INTO `reveloper_tareascompletadas` VALUES (1,'TP1','Tarea prueba 1','2024-11-22 03:00:00.000000','completada','Tarea completada y transferida automáticamente.',3),(2,'T1','Analisis del problema','2024-11-23 03:00:00.000000','completada','Tarea completada y transferida automáticamente.',2),(3,'T2','Diseño de base de datos','2024-11-23 03:00:00.000000','completada','Tarea completada y transferida automáticamente.',2),(4,'TP1','Tarea prueba 1','2024-11-22 03:00:00.000000','completada','Tarea completada y transferida automáticamente.',3),(5,'HTMLPW1','Crear la plantilla HTML','2024-11-30 03:00:00.000000','completada','Tarea completada y transferida automáticamente.',2),(6,'test001','Tarea de Prueba','2024-11-24 03:00:00.000000','completada','Tarea completada y transferida automáticamente.',2),(7,'TP3','tarea prueba 3','2024-11-30 03:00:00.000000','completada','Tarea completada y transferida automáticamente.',2),(8,'OLSR1','Funcionalidad obtener liquidaciones','2024-11-30 03:00:00.000000','completada','Tarea completada y transferida automáticamente.',4),(9,'ISSR1','Funcionalidad informes sociales Salud','2024-11-27 03:00:00.000000','completada','Tarea completada y transferida automáticamente.',4),(10,'LEC1','Login Ecommerce1','2024-11-30 03:00:00.000000','completada','Tarea completada y transferida automáticamente.',3);
/*!40000 ALTER TABLE `reveloper_tareascompletadas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reveloper_usuario`
--

DROP TABLE IF EXISTS `reveloper_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reveloper_usuario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `nombre` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `apellido` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `tareas_completadas` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reveloper_usuario`
--

LOCK TABLES `reveloper_usuario` WRITE;
/*!40000 ALTER TABLE `reveloper_usuario` DISABLE KEYS */;
INSERT INTO `reveloper_usuario` VALUES (1,'pbkdf2_sha256$870000$UHUmp03yQyxxngyGg2qbJj$5XZY7xL2RpQWyvXOIV+VZFC0z2rpIi6LdRKcM0i77+I=','2024-11-24 19:11:41.140449',1,'admin','Admin','Reveloper','admin@reveloper.com',1,1,'2024-11-17 20:13:35.000000','','','2024-11-17 20:13:35.866556',0),(2,'pbkdf2_sha256$870000$Sf3u9K9jYwJMKNXJwJFZyu$Tazyv0sD1+iyj59docz/RFiqqFT2yPa52qf6oSDfBvY=','2024-11-24 18:06:30.698847',0,'Developer1','Roberto Emilio','González Guzmán','developer1@reveloper.com',0,1,'2024-11-17 22:55:02.000000','','','2024-11-17 22:55:02.900689',4),(3,'pbkdf2_sha256$870000$zsS8wDfDBZLS3TAOU4qKsM$Au0aKp76U632zIZ5rMuvSxLyxtVnfod6uxk207BXkMM=','2024-11-24 19:15:42.908683',0,'Developer2','Pedro','Villegas','developer2@reveloper.com',0,1,'2024-11-18 18:10:44.000000','','','2024-11-18 18:10:45.771775',2),(4,'pbkdf2_sha256$870000$K0uXkgihP5E7XoP8DGZdP0$aBduZTLgMDPtOa7wbUJnITBnjjMdnQSM+ieZBjhRGzM=','2024-11-24 18:55:03.390689',0,'Developer3','María','Quiroz','developer3@reveloper.com',0,1,'2024-11-21 13:15:12.000000','','','2024-11-21 13:15:13.603530',2);
/*!40000 ALTER TABLE `reveloper_usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reveloper_usuario_groups`
--

DROP TABLE IF EXISTS `reveloper_usuario_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reveloper_usuario_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Reveloper_usuario_groups_usuario_id_group_id_ca479a26_uniq` (`usuario_id`,`group_id`),
  KEY `Reveloper_usuario_groups_group_id_35487c82_fk_auth_group_id` (`group_id`),
  CONSTRAINT `Reveloper_usuario_gr_usuario_id_22da7909_fk_Reveloper` FOREIGN KEY (`usuario_id`) REFERENCES `reveloper_usuario` (`id`),
  CONSTRAINT `Reveloper_usuario_groups_group_id_35487c82_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reveloper_usuario_groups`
--

LOCK TABLES `reveloper_usuario_groups` WRITE;
/*!40000 ALTER TABLE `reveloper_usuario_groups` DISABLE KEYS */;
INSERT INTO `reveloper_usuario_groups` VALUES (1,1,1),(2,1,2),(3,2,1),(4,3,1),(5,4,1);
/*!40000 ALTER TABLE `reveloper_usuario_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reveloper_usuario_user_permissions`
--

DROP TABLE IF EXISTS `reveloper_usuario_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reveloper_usuario_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Reveloper_usuario_user_p_usuario_id_permission_id_41d1a696_uniq` (`usuario_id`,`permission_id`),
  KEY `Reveloper_usuario_us_permission_id_2880de33_fk_auth_perm` (`permission_id`),
  CONSTRAINT `Reveloper_usuario_us_permission_id_2880de33_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `Reveloper_usuario_us_usuario_id_776917cf_fk_Reveloper` FOREIGN KEY (`usuario_id`) REFERENCES `reveloper_usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reveloper_usuario_user_permissions`
--

LOCK TABLES `reveloper_usuario_user_permissions` WRITE;
/*!40000 ALTER TABLE `reveloper_usuario_user_permissions` DISABLE KEYS */;
INSERT INTO `reveloper_usuario_user_permissions` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7),(8,1,8),(9,1,9),(10,1,10),(11,1,11),(12,1,12),(13,1,13),(14,1,14),(15,1,15),(16,1,16),(17,1,17),(18,1,18),(19,1,19),(20,1,20),(21,1,21),(22,1,22),(23,1,23),(24,1,24),(25,1,25),(26,1,26),(27,1,27),(28,1,28),(29,1,29),(30,1,30),(31,1,31),(32,1,32),(33,1,33),(34,1,34),(35,1,35),(36,1,36),(37,1,37),(38,1,38),(39,1,39),(40,1,40),(41,2,44);
/*!40000 ALTER TABLE `reveloper_usuario_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-24 16:30:45
