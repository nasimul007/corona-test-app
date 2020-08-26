-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 26, 2020 at 06:47 PM
-- Server version: 10.1.38-MariaDB
-- PHP Version: 7.3.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `coronatest`
--

-- --------------------------------------------------------

--
-- Table structure for table `coronadbs`
--

CREATE TABLE `coronadbs` (
  `sl_no` int(11) NOT NULL,
  `age` int(50) NOT NULL,
  `sex` varchar(50) NOT NULL,
  `temperature` varchar(50) NOT NULL,
  `assessment_date` date NOT NULL,
  `assessment_score` int(50) NOT NULL,
  `result` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `coronadbs`
--

INSERT INTO `coronadbs` (`sl_no`, `age`, `sex`, `temperature`, `assessment_date`, `assessment_score`, `result`) VALUES
(1, 54, 'male', '100', '2020-08-26', 11, 'Positive'),
(2, 22, 'female', '38', '2020-08-26', 10, 'Positive'),
(3, 11, 'male', '29', '2020-08-26', 3, 'Negative'),
(4, 11, 'male', '100', '2020-08-26', 5, 'Positive'),
(5, 11, 'male', '30', '2020-08-26', 0, 'Negative'),
(6, 12, 'male', '30', '2020-08-26', 0, 'Negative'),
(7, 13, 'male', '40', '2020-08-26', 6, 'Positive'),
(8, 13, 'male', '40', '2020-08-26', 5, 'Positive'),
(9, 13, 'male', '40', '2020-08-26', 6, 'Positive'),
(10, 13, 'male', '40', '2020-08-26', 6, 'Positive'),
(11, 99, 'male', '33', '2020-08-26', 4, 'Negative'),
(12, 80, 'male', '33', '2020-08-26', 5, 'Positive'),
(13, 55, 'male', '40', '2020-08-26', 16, 'Positive'),
(14, 44, 'male', '23', '2020-08-26', 7, 'Positive'),
(15, 44, 'male', '23', '2020-08-26', 7, 'Positive'),
(16, 23, 'male', '23', '2020-08-26', 7, 'Positive'),
(17, 46, 'male', '100', '2020-08-26', 11, 'Positive'),
(18, 88, 'female', '100', '2020-08-26', 10, 'Positive'),
(19, 99, 'Male', '40', '2020-08-26', 8, 'Positive'),
(20, 22, 'Male', '40', '2020-08-26', 9, 'Positive');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `coronadbs`
--
ALTER TABLE `coronadbs`
  ADD PRIMARY KEY (`sl_no`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `coronadbs`
--
ALTER TABLE `coronadbs`
  MODIFY `sl_no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
