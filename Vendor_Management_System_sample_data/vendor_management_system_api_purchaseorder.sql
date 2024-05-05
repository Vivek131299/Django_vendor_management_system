-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: vendor_management_system
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `api_purchaseorder`
--

DROP TABLE IF EXISTS `api_purchaseorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_purchaseorder` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `po_number` varchar(10) NOT NULL,
  `order_date` date NOT NULL,
  `delivery_date` date NOT NULL,
  `items` json NOT NULL,
  `quantity` int NOT NULL,
  `status` varchar(20) NOT NULL,
  `quality_rating` double DEFAULT NULL,
  `issue_date` datetime(6) NOT NULL,
  `acknowledgment_date` datetime(6) DEFAULT NULL,
  `vendor_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_purchaseorder_vendor_id_3dfc4286_fk_api_vendor_id` (`vendor_id`),
  CONSTRAINT `api_purchaseorder_vendor_id_3dfc4286_fk_api_vendor_id` FOREIGN KEY (`vendor_id`) REFERENCES `api_vendor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_purchaseorder`
--

LOCK TABLES `api_purchaseorder` WRITE;
/*!40000 ALTER TABLE `api_purchaseorder` DISABLE KEYS */;
INSERT INTO `api_purchaseorder` VALUES (16,'0537194339','2024-04-20','2024-05-01','[{\"name\": \"Dell laptop\", \"price\": 60000}, {\"name\": \"Cricket set\", \"price\": 5000}]',2,'Completed',NULL,'2024-05-02 09:47:03.526167','2024-05-02 15:18:14.225551',2),(17,'7141959281','2024-05-02','2024-05-02','[{\"name\": \"Apple iPhone 15\", \"price\": 80000}]',1,'Completed',NULL,'2024-05-02 09:50:00.362538','2024-05-02 15:20:10.402749',2),(18,'4825081481','2024-05-02','2024-05-02','[{\"name\": \"Samsung S24 Ultra\", \"price\": 90000}]',1,'Completed',50,'2024-05-02 10:42:05.259555','2024-05-02 16:12:23.546188',2),(19,'0468156172','2024-05-02','2024-05-02','[{\"name\": \"Lenovo Yoga i5\", \"price\": 75000}, {\"name\": \"Logitech Mouse\", \"price\": 500}, {\"name\": \"Xiaomi Powerbank 1000mah\", \"price\": \"1500\"}]',3,'Completed',80,'2024-05-02 11:30:08.453852','2024-05-02 17:00:29.231891',2),(20,'2277373327','2024-05-02','2024-05-09','[{\"name\": \"Xiaomi Powerbank 1000mah\", \"price\": \"1500\"}]',1,'Completed',30,'2024-05-02 12:11:54.469756','2024-05-03 13:50:12.838701',2),(21,'2439730466','2024-05-02','2024-05-09','[{\"name\": \"Lenovo Yoga i5\", \"price\": 75000}]',1,'Completed',100,'2024-05-02 12:25:21.472630','2024-05-02 17:59:26.072042',2),(22,'5909130826','2024-05-02','2024-05-09','[{\"name\": \"Lenovo Yoga i5\", \"price\": 75000}]',1,'Completed',100,'2024-05-02 17:59:54.189355','2024-05-03 12:16:06.975099',2),(23,'0689912997','2024-05-03','2024-05-10','[{\"name\": \"Motorola Edge 50\", \"price\": 30000}, {\"name\": \"Airpods pro\", \"price\": 20000}]',2,'Completed',30,'2024-05-03 17:02:49.498846','2024-05-03 17:03:32.134733',2),(24,'5542395554','2024-05-03','2024-05-10','[{\"name\": \"Airpods pro\", \"price\": 20000}]',1,'Completed',80,'2024-05-03 20:03:01.939102','2024-05-03 20:33:03.035735',2),(25,'3161327783','2024-05-03','2024-05-10','[{\"name\": \"Airpods pro\", \"price\": 20000}]',1,'Completed',80,'2024-05-03 20:30:16.373068',NULL,2),(26,'1148190990','2024-05-03','2024-05-10','[{\"name\": \"Airpods pro\", \"price\": 20000}]',1,'Completed',80,'2024-05-03 20:31:55.458762',NULL,2),(27,'0326921797','2024-05-03','2024-05-10','[{\"name\": \"Airpods pro\", \"price\": 20000}]',1,'Completed',90,'2024-05-03 20:36:23.224443','2024-05-03 21:37:46.587192',2),(28,'3027003889','2024-05-03','2024-05-10','[{\"name\": \"Airpods pro\", \"price\": 20000}]',1,'Completed',90,'2024-05-03 20:38:35.672795',NULL,2),(29,'3880693527','2024-05-03','2024-05-10','[{\"name\": \"Airpods pro\", \"price\": 20000}]',1,'Completed',90,'2024-05-03 20:39:05.144834',NULL,2),(30,'1552868407','2024-05-03','2024-05-10','[{\"name\": \"Airpods pro\", \"price\": 20000}]',1,'Pending',NULL,'2024-05-03 20:39:45.132353',NULL,2),(31,'2837899747','2024-05-03','2024-05-10','[{\"name\": \"Airpods pro\", \"price\": 20000}]',1,'Pending',NULL,'2024-05-03 20:42:34.237821',NULL,2),(32,'1480552498','2024-05-03','2024-05-10','[{\"name\": \"Airpods pro\", \"price\": 20000}]',1,'Pending',NULL,'2024-05-03 20:44:33.747465',NULL,2),(33,'0050583096','2024-05-03','2024-05-10','[{\"name\": \"Airpods pro\", \"price\": 20000}]',1,'Pending',NULL,'2024-05-03 21:35:49.383151',NULL,2);
/*!40000 ALTER TABLE `api_purchaseorder` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-05 16:20:33
