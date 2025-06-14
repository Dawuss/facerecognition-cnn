-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 14, 2025 at 06:14 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sistem_presensi`
--

-- --------------------------------------------------------

--
-- Table structure for table `daftar_kelas`
--

CREATE TABLE `daftar_kelas` (
  `id` int(11) NOT NULL,
  `kelas_id` int(11) NOT NULL,
  `matakuliah_id` int(11) NOT NULL,
  `tanggal` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `daftar_kelas`
--

INSERT INTO `daftar_kelas` (`id`, `kelas_id`, `matakuliah_id`, `tanggal`) VALUES
(7, 1, 2, '2025-06-05'),
(8, 1, 2, '2025-06-06'),
(9, 1, 3, '2025-06-06'),
(10, 1, 2, '2025-06-07'),
(11, 1, 2, '2025-06-08'),
(12, 1, 3, '2025-06-08'),
(13, 1, 2, '2025-06-09'),
(14, 1, 2, '2025-06-10'),
(15, 1, 3, '2025-06-09'),
(16, 1, 3, '2025-06-10'),
(17, 1, 2, '2025-06-11'),
(18, 1, 3, '2025-06-11'),
(19, 1, 5, '2025-06-14');

-- --------------------------------------------------------

--
-- Table structure for table `kelas`
--

CREATE TABLE `kelas` (
  `id` int(11) NOT NULL,
  `nama_kelas` varchar(255) NOT NULL,
  `semester` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kelas`
--

INSERT INTO `kelas` (`id`, `nama_kelas`, `semester`) VALUES
(1, 'MIB', 8),
(2, 'MIC', 8);

-- --------------------------------------------------------

--
-- Table structure for table `mahasiswa`
--

CREATE TABLE `mahasiswa` (
  `id_mahasiswa` varchar(20) NOT NULL,
  `nama_mahasiswa` varchar(255) NOT NULL,
  `kelas_id` int(11) NOT NULL,
  `semester` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mahasiswa`
--

INSERT INTO `mahasiswa` (`id_mahasiswa`, `nama_mahasiswa`, `kelas_id`, `semester`) VALUES
('062040832695', 'Muhammad Rafi Athallah', 1, 8),
('062140830469', 'Aisyah Wulan Dari', 1, 8),
('062140830470', 'Emilia Fransiska', 1, 8),
('062140830471', 'Ilham Saleh', 1, 8),
('062140830472', 'Sella', 1, 8),
('062140830473', 'Serli Monica', 1, 8),
('062140830474', 'Tona Lestari', 1, 8),
('062140830475', 'Violin Annisa Ramadhani', 1, 8),
('062140832893', 'Arya Thomas', 1, 8),
('062140832894', 'Azzahra Karindiva', 1, 8),
('062140832895', 'Dila Puspitasari', 1, 8),
('062140832896', 'Dody Ardiansyah', 1, 8),
('062140832897', 'Feni Mutia', 1, 8),
('062140832898', 'Ferdinan Sastra Anggara', 1, 8),
('062140832899', 'Laras Anggi Wijayanti', 1, 8),
('062140832900', 'M. Putra Pamungkas', 1, 8),
('062140832901', 'Marsellina', 1, 8),
('062140832903', 'Muhammad Kannu Santara', 1, 8),
('062140832904', 'Rafika Ayu', 1, 8),
('062140832906', 'Risky Firdaus', 1, 8),
('062140832907', 'Sina Widianti', 1, 8),
('062140832908', 'Vikken Aghenta Pradana', 1, 8),
('062140832909', 'Wulan Restu Utami', 1, 8),
('062140832910', 'Zahrany Mega Lestari', 1, 8);

-- --------------------------------------------------------

--
-- Table structure for table `matakuliah`
--

CREATE TABLE `matakuliah` (
  `id_mk` int(11) NOT NULL,
  `kode` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `dosen_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `matakuliah`
--

INSERT INTO `matakuliah` (`id_mk`, `kode`, `nama`, `dosen_id`) VALUES
(2, 'MF201825', 'Data Mining', 5),
(3, 'MF201808', 'Manajemen Resiko', 6),
(5, 'MF201806', 'Bisnis Elektronik (E-Bisnis)', 7);

-- --------------------------------------------------------

--
-- Table structure for table `presensi`
--

CREATE TABLE `presensi` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `tanggal` date NOT NULL,
  `kelas_id` int(11) NOT NULL,
  `waktu_masuk` time NOT NULL,
  `status` enum('hadir','izin','sakit','alpha') DEFAULT 'alpha',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `matakuliah_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `presensi`
--

INSERT INTO `presensi` (`id`, `nama`, `tanggal`, `kelas_id`, `waktu_masuk`, `status`, `created_at`, `matakuliah_id`) VALUES
(76, 'Emilia Fransiska', '2025-06-09', 1, '18:36:50', '', '2025-06-06 11:36:50', 2),
(77, 'Aisyah Wulan Dari', '2025-06-09', 1, '18:40:35', 'hadir', '2025-06-06 11:40:35', 2),
(78, 'Feni Mutia', '2025-06-09', 1, '18:40:35', 'hadir', '2025-06-06 11:40:35', 2),
(79, 'Ilham Saleh', '2025-06-09', 1, '18:40:36', 'hadir', '2025-06-06 11:40:36', 2),
(80, 'Muhammad Rafi Athallah', '2025-06-09', 1, '18:40:36', 'hadir', '2025-06-06 11:40:36', 2),
(81, 'Marsellina', '2025-06-09', 1, '18:40:37', 'hadir', '2025-06-06 11:40:37', 2),
(82, 'Wulan Restu Utami', '2025-06-09', 1, '18:40:37', 'hadir', '2025-06-06 11:40:37', 2),
(83, 'M. Putra Pamungkas', '2025-06-09', 1, '18:40:37', 'hadir', '2025-06-06 11:40:37', 2),
(84, 'Laras Anggi Wijayanti', '2025-06-09', 1, '18:40:38', 'hadir', '2025-06-06 11:40:38', 2),
(85, 'Azzahra Karindiva', '2025-06-09', 1, '18:40:38', 'hadir', '2025-06-06 11:40:38', 2),
(86, 'Vikken Aghenta Pradana', '2025-06-09', 1, '18:40:39', 'hadir', '2025-06-06 11:40:39', 2),
(87, 'Arya Thomas', '2025-06-09', 1, '18:40:39', 'hadir', '2025-06-06 11:40:39', 2),
(88, 'Ferdinan Sastra Anggara', '2025-06-09', 1, '18:40:39', 'hadir', '2025-06-06 11:40:39', 2),
(89, 'Muhammad Kannu Santara', '2025-06-09', 1, '18:40:40', 'hadir', '2025-06-06 11:40:40', 2),
(90, 'Zahrany Mega Lestari', '2025-06-09', 1, '18:40:40', 'hadir', '2025-06-06 11:40:40', 2),
(91, 'Sina Widianti', '2025-06-09', 1, '18:40:41', 'hadir', '2025-06-06 11:40:41', 2),
(92, 'Serli Monica', '2025-06-09', 1, '18:40:41', 'hadir', '2025-06-06 11:40:41', 2),
(93, 'Rafika Ayu', '2025-06-09', 1, '18:40:41', 'hadir', '2025-06-06 11:40:41', 2),
(94, 'Dila Puspitasari', '2025-06-09', 1, '18:40:42', 'hadir', '2025-06-06 11:40:42', 2),
(95, 'Tona Lestari', '2025-06-09', 1, '18:40:42', 'hadir', '2025-06-06 11:40:42', 2),
(96, 'Sella', '2025-06-09', 1, '18:40:43', 'hadir', '2025-06-06 11:40:43', 2),
(97, 'Violin Annisa Ramadhani', '2025-06-09', 1, '18:40:43', 'hadir', '2025-06-06 11:40:43', 2),
(98, 'Risky Firdaus', '2025-06-09', 1, '18:40:43', 'hadir', '2025-06-06 11:40:43', 2),
(99, 'Dody Ardiansyah', '2025-06-09', 1, '18:40:44', 'hadir', '2025-06-06 11:40:44', 2),
(100, 'Aisyah Wulan Dari', '2025-06-10', 1, '14:00:29', 'hadir', '2025-06-09 07:00:29', 2),
(101, 'Feni Mutia', '2025-06-09', 1, '14:02:46', 'hadir', '2025-06-09 07:02:46', 3),
(102, 'Ilham Saleh', '2025-06-09', 1, '14:02:46', 'hadir', '2025-06-09 07:02:46', 3),
(103, 'Muhammad Rafi Athallah', '2025-06-09', 1, '14:02:47', 'hadir', '2025-06-09 07:02:47', 3),
(104, 'Marsellina', '2025-06-09', 1, '14:02:47', 'hadir', '2025-06-09 07:02:47', 3),
(105, 'Wulan Restu Utami', '2025-06-09', 1, '14:02:48', 'hadir', '2025-06-09 07:02:48', 3),
(106, 'M. Putra Pamungkas', '2025-06-09', 1, '14:02:48', 'hadir', '2025-06-09 07:02:48', 3),
(107, 'Dody Ardiansyah', '2025-06-09', 1, '14:02:49', 'hadir', '2025-06-09 07:02:49', 3),
(108, 'Laras Anggi Wijayanti', '2025-06-09', 1, '14:02:49', 'hadir', '2025-06-09 07:02:49', 3),
(109, 'Azzahra Karindiva', '2025-06-09', 1, '14:02:49', 'hadir', '2025-06-09 07:02:49', 3),
(110, 'Vikken Aghenta Pradana', '2025-06-09', 1, '14:02:50', 'hadir', '2025-06-09 07:02:50', 3),
(111, 'Arya Thomas', '2025-06-09', 1, '14:02:50', 'hadir', '2025-06-09 07:02:50', 3),
(112, 'Ferdinan Sastra Anggara', '2025-06-09', 1, '14:02:51', 'hadir', '2025-06-09 07:02:51', 3),
(113, 'Muhammad Kannu Santara', '2025-06-09', 1, '14:02:51', 'hadir', '2025-06-09 07:02:51', 3),
(114, 'Zahrany Mega Lestari', '2025-06-09', 1, '14:02:51', 'hadir', '2025-06-09 07:02:51', 3),
(115, 'Sina Widianti', '2025-06-09', 1, '14:02:52', 'hadir', '2025-06-09 07:02:52', 3),
(116, 'Serli Monica', '2025-06-09', 1, '14:02:52', 'hadir', '2025-06-09 07:02:52', 3),
(117, 'Rafika Ayu', '2025-06-09', 1, '14:02:53', 'hadir', '2025-06-09 07:02:53', 3),
(118, 'Dila Puspitasari', '2025-06-09', 1, '14:02:53', 'hadir', '2025-06-09 07:02:53', 3),
(119, 'Tona Lestari', '2025-06-09', 1, '14:02:53', 'hadir', '2025-06-09 07:02:53', 3),
(120, 'Sella', '2025-06-09', 1, '14:02:54', 'hadir', '2025-06-09 07:02:54', 3),
(121, 'Violin Annisa Ramadhani', '2025-06-09', 1, '14:02:54', 'hadir', '2025-06-09 07:02:54', 3),
(122, 'Risky Firdaus', '2025-06-09', 1, '14:02:55', 'hadir', '2025-06-09 07:02:55', 3),
(123, 'Aisyah Wulan Dari', '2025-06-09', 1, '14:03:18', 'alpha', '2025-06-09 07:03:18', 3),
(124, 'Emilia Fransiska', '2025-06-09', 1, '14:03:27', 'sakit', '2025-06-09 07:03:27', 3),
(125, 'Emilia Fransiska', '2025-06-10', 1, '16:53:48', 'hadir', '2025-06-09 09:53:48', 3),
(126, 'Aisyah Wulan Dari', '2025-06-10', 1, '16:53:48', 'hadir', '2025-06-09 09:53:48', 3),
(127, 'Feni Mutia', '2025-06-10', 1, '16:53:48', 'hadir', '2025-06-09 09:53:48', 3),
(128, 'Ilham Saleh', '2025-06-10', 1, '16:53:49', 'hadir', '2025-06-09 09:53:49', 3),
(129, 'Muhammad Rafi Athallah', '2025-06-10', 1, '16:53:49', 'hadir', '2025-06-09 09:53:49', 3),
(130, 'Marsellina', '2025-06-10', 1, '16:53:49', 'hadir', '2025-06-09 09:53:49', 3),
(131, 'Wulan Restu Utami', '2025-06-10', 1, '16:53:49', 'hadir', '2025-06-09 09:53:49', 3),
(132, 'M. Putra Pamungkas', '2025-06-10', 1, '16:53:50', 'hadir', '2025-06-09 09:53:50', 3),
(133, 'Dody Ardiansyah', '2025-06-10', 1, '16:53:50', 'hadir', '2025-06-09 09:53:50', 3),
(134, 'Laras Anggi Wijayanti', '2025-06-10', 1, '16:53:50', 'hadir', '2025-06-09 09:53:50', 3),
(135, 'Azzahra Karindiva', '2025-06-10', 1, '16:53:50', 'hadir', '2025-06-09 09:53:50', 3),
(136, 'Vikken Aghenta Pradana', '2025-06-10', 1, '16:53:51', 'hadir', '2025-06-09 09:53:51', 3),
(137, 'Arya Thomas', '2025-06-10', 1, '16:53:51', 'hadir', '2025-06-09 09:53:51', 3),
(138, 'Ferdinan Sastra Anggara', '2025-06-10', 1, '16:53:53', 'hadir', '2025-06-09 09:53:53', 3),
(139, 'Muhammad Kannu Santara', '2025-06-10', 1, '16:53:53', 'hadir', '2025-06-09 09:53:53', 3),
(140, 'Zahrany Mega Lestari', '2025-06-10', 1, '16:53:53', 'hadir', '2025-06-09 09:53:53', 3),
(141, 'Sina Widianti', '2025-06-10', 1, '16:53:53', 'hadir', '2025-06-09 09:53:53', 3),
(142, 'Serli Monica', '2025-06-10', 1, '16:53:54', 'hadir', '2025-06-09 09:53:54', 3),
(143, 'Rafika Ayu', '2025-06-10', 1, '16:53:54', 'hadir', '2025-06-09 09:53:54', 3),
(144, 'Dila Puspitasari', '2025-06-10', 1, '16:53:54', 'hadir', '2025-06-09 09:53:54', 3),
(145, 'Tona Lestari', '2025-06-10', 1, '16:53:54', 'hadir', '2025-06-09 09:53:54', 3),
(146, 'Risky Firdaus', '2025-06-10', 1, '16:53:55', 'hadir', '2025-06-09 09:53:55', 3),
(147, 'Violin Annisa Ramadhani', '2025-06-10', 1, '16:54:20', 'sakit', '2025-06-09 09:54:20', 3),
(148, 'Sella', '2025-06-10', 1, '16:54:28', 'izin', '2025-06-09 09:54:28', 3),
(149, 'Emilia Fransiska', '2025-06-14', 1, '12:32:28', 'hadir', '2025-06-14 05:32:28', 5),
(150, 'Aisyah Wulan Dari', '2025-06-14', 1, '12:32:29', 'hadir', '2025-06-14 05:32:29', 5),
(151, 'Feni Mutia', '2025-06-14', 1, '12:32:29', 'hadir', '2025-06-14 05:32:29', 5),
(152, 'Ilham Saleh', '2025-06-14', 1, '12:32:29', 'hadir', '2025-06-14 05:32:29', 5),
(153, 'Muhammad Rafi Athallah', '2025-06-14', 1, '12:32:30', 'hadir', '2025-06-14 05:32:30', 5),
(154, 'Marsellina', '2025-06-14', 1, '12:32:30', 'hadir', '2025-06-14 05:32:30', 5),
(155, 'Wulan Restu Utami', '2025-06-14', 1, '12:32:31', 'hadir', '2025-06-14 05:32:31', 5),
(156, 'M. Putra Pamungkas', '2025-06-14', 1, '12:32:31', 'hadir', '2025-06-14 05:32:31', 5),
(157, 'Dody Ardiansyah', '2025-06-14', 1, '12:32:32', 'hadir', '2025-06-14 05:32:32', 5),
(158, 'Laras Anggi Wijayanti', '2025-06-14', 1, '12:32:32', 'hadir', '2025-06-14 05:32:32', 5),
(159, 'Azzahra Karindiva', '2025-06-14', 1, '12:32:33', 'hadir', '2025-06-14 05:32:33', 5),
(160, 'Vikken Aghenta Pradana', '2025-06-14', 1, '12:32:33', 'hadir', '2025-06-14 05:32:33', 5),
(161, 'Arya Thomas', '2025-06-14', 1, '12:32:34', 'hadir', '2025-06-14 05:32:34', 5),
(162, 'Ferdinan Sastra Anggara', '2025-06-14', 1, '12:32:34', 'hadir', '2025-06-14 05:32:34', 5),
(163, 'Muhammad Kannu Santara', '2025-06-14', 1, '12:32:34', 'hadir', '2025-06-14 05:32:35', 5),
(164, 'Zahrany Mega Lestari', '2025-06-14', 1, '12:32:35', 'hadir', '2025-06-14 05:32:35', 5),
(165, 'Sina Widianti', '2025-06-14', 1, '12:32:35', 'hadir', '2025-06-14 05:32:35', 5),
(166, 'Serli Monica', '2025-06-14', 1, '12:32:36', 'hadir', '2025-06-14 05:32:36', 5),
(167, 'Rafika Ayu', '2025-06-14', 1, '12:32:36', 'hadir', '2025-06-14 05:32:36', 5),
(168, 'Dila Puspitasari', '2025-06-14', 1, '12:32:37', 'hadir', '2025-06-14 05:32:37', 5),
(169, 'Tona Lestari', '2025-06-14', 1, '12:32:37', 'hadir', '2025-06-14 05:32:37', 5),
(170, 'Sella', '2025-06-14', 1, '12:32:37', 'hadir', '2025-06-14 05:32:37', 5),
(171, 'Violin Annisa Ramadhani', '2025-06-14', 1, '12:32:38', 'hadir', '2025-06-14 05:32:38', 5),
(172, 'Risky Firdaus', '2025-06-14', 1, '12:32:38', 'hadir', '2025-06-14 05:32:38', 5);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('mahasiswa','dosen','admin') NOT NULL,
  `nama_lengkap` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`, `nama_lengkap`, `email`, `created_at`) VALUES
(3, 'Admin', '$2b$12$BFSvSyPFrIH5L3B55FPdLuymbgpTvjTTp4k7yucazAcD/WWkR5EBa', 'admin', 'JurusanMi', 'mi@polsri.ac.id', '2025-05-26 06:29:30'),
(4, '062140832906', '$2b$12$rmd4KX043Ly8m6ypgTT7NuGd5M09q.U73u.VWeY.lVmHJ3rZKbXHq', 'mahasiswa', 'Risky Firdaus', 'daus.riskyfirdaus@gmail.com', '2025-05-26 06:34:33'),
(5, '0214018101', '$2b$12$8SZDnCshhgF9EyG30NuQtOYeSQxGbZLpWuTXf6vSzNfLLWmtrzHAa', 'dosen', 'Muhammad Aris Ganiardi, S.Si., M.T.', 'aris@polsri.ac.id', '2025-05-26 06:37:37'),
(6, '0023117410', '$2b$12$EdRFZqtWbkHSmOF0Hvsp6uG6KsEIvJHKM.nwKbPGnri0j0oU4cmlW', 'dosen', 'Nita Novita, S.E., M.M.', 'nitanovita@polsri.ac.id', '2025-05-26 11:45:10'),
(7, '0014057906', '$2b$12$4yg1jxshNHlWEoEOj8cjZeydmi8C1y9qrBA/Q0hlsEunE7lo1Flh2', 'dosen', 'Dr. Hetty Meileni, S.Kom., M.T.', 'hetty@polsri.ac.id', '2025-06-14 03:55:10');

-- --------------------------------------------------------

--
-- Table structure for table `user_tokens`
--

CREATE TABLE `user_tokens` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `token_hash` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `expired_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_tokens`
--

INSERT INTO `user_tokens` (`id`, `user_id`, `token_hash`, `created_at`, `expired_at`) VALUES
(1, 3, '$2b$12$9iB3YnUlpZHpqO5dsp58ZeuBJm8Ksvhg07clzLoUsQZwJBTHJm86i', '2025-05-26 06:45:49', '2025-05-27 06:45:49'),
(2, 3, '$2b$12$mcqNdO9LvyjOyLycRabFk.sOIk7uUgCM9PyI5Wzk4k3ZNQm8NGr..', '2025-05-26 06:49:10', '2025-05-27 06:49:10'),
(4, 4, '$2b$12$W2Tukgl7kH.UCNec0O3GseFtl0F63/MJ/5ATX4ZyS.REhzSihfRra', '2025-05-26 06:52:02', '2025-05-27 06:52:02'),
(5, 3, '$2b$12$bSYo9BtqzInZ4nXGWziPseMfByuP6lOswqYwZPXSDnBA5/0SqgIcO', '2025-05-26 06:56:51', '2025-05-27 06:56:51'),
(6, 3, '$2b$12$Z4jcuYxqwcdj93U6BJMbTO2DmjCfmcUqVk4uMsb.phQm2JokPzmiC', '2025-05-26 07:00:55', '2025-05-27 07:00:55'),
(8, 5, '$2b$12$DVVViNYefQK5qd2y/hGH.ON5aWQQ8PKn4ycmQwsnwl8wAVUJJAa4W', '2025-05-26 07:06:42', '2025-05-27 07:06:42'),
(9, 4, '$2b$12$u0dTjFQg5uQTZWvIgc9SHeSTxEX7ewdTRRx9bRuZ7z4PUNLtJEC5e', '2025-05-26 07:07:37', '2025-05-27 07:07:37'),
(10, 4, '$2b$12$b2PTOHd2iCHbZCGOGA/uPu2YxAKIDTsnIF02cNjPtKyofiNf8AxEm', '2025-05-26 07:14:28', '2025-05-27 07:14:28'),
(11, 4, '$2b$12$zyohwRwrQl3j38L3fuS5Beld8h0jG6/KwNmPrr08gWq78XJwVJur6', '2025-05-26 07:19:12', '2025-05-27 07:19:12'),
(13, 5, '$2b$12$DmOyB.BM0Ou/cwqFWLYlm.0U.WUmqhQ9yba2tmKtJ.OL3vSlVgF9y', '2025-05-26 07:22:37', '2025-05-27 07:22:37'),
(15, 3, '$2b$12$LXJEKFJ24BQ1YCvn7RZtHuOFAm7UR0R8OfPwV8h1Sg8PFmZFdNsne', '2025-05-26 11:09:19', '2025-05-27 11:09:19'),
(16, 3, '$2b$12$RsNK1p5V5/cIhvSgh5L/2.JrkGBS/j7cUuBotEYQTS26xc0.S4Z/W', '2025-05-26 11:14:14', '2025-05-27 11:14:14'),
(17, 3, '$2b$12$3Fwc39b.jV4XG83AxGsFjeQe6PvswIBdkc1IKR37axUbc0V7VYm6a', '2025-05-26 11:17:45', '2025-05-27 11:17:45'),
(22, 3, '$2b$12$BLeo.FHUI55yMicoW9jsDO/96ef/hTri/RbPTDTtCm47XaqEjN0rm', '2025-05-26 12:53:48', '2025-05-27 12:53:48'),
(25, 3, '$2b$12$tNpvv7vDkthznOoui8Fy1uhuCP67kRSEasJrzJ4uDMqjo2Ew9Vi8.', '2025-05-26 15:54:24', '2025-05-27 15:54:24'),
(26, 4, '$2b$12$BrhG1frSTINGNA9qWRhwUuahFZjElIlACyCPCxwX5pmy1EJ9U2Lca', '2025-05-28 03:33:16', '2025-05-29 03:33:16'),
(27, 4, '$2b$12$iAqpK4G3ZLiL5EOhRaB78.gjkC/0tC0HP3BFzfurgF9G4PR.aWh1C', '2025-05-29 07:53:05', '2025-05-30 07:53:05'),
(28, 4, '$2b$12$/g7Py6ZDvHe4EglcFzMbjOuu0WHORCUnIPXdt6oD0TW2gJRnUDY9S', '2025-06-05 06:27:01', '2025-06-06 06:27:01'),
(30, 4, '$2b$12$R0Stmf3wu/PWRCDepAORx./h72Dab1RoJV3zvyO/xu5FcEhHlwXQi', '2025-06-05 06:54:41', '2025-06-06 06:54:41'),
(31, 4, '$2b$12$k02WVtxBtioWY8XkS5j1MuJjHXDrHfPKLYB1kiHMRzqvWe/MjiX2K', '2025-06-05 07:16:05', '2025-06-06 07:16:05'),
(32, 4, '$2b$12$LiAMqExP2QJhOp4htTWN2OShGShSRxqFHeHhX7wjt8uJHBl31eJuu', '2025-06-05 07:36:43', '2025-06-06 07:36:43'),
(34, 3, '$2b$12$EmUP9BQWUQSHzz1aseD0ZuMQLcKVFqQZPSupz8Ur4ZRnPAJ3rOAfq', '2025-06-05 07:43:57', '2025-06-06 07:43:57'),
(36, 4, '$2b$12$yFm9vze.S2TW0f7baRNVvOSm7590BI2JevnzmJSbfiSHmtX8XVFYG', '2025-06-05 08:15:36', '2025-06-06 08:15:36'),
(37, 4, '$2b$12$6qb0Le.JDMGW4B54Js1GjODkF7ny7RvDFauG5fQ8VPGmw36gd8VZ6', '2025-06-05 08:35:52', '2025-06-06 08:35:52'),
(38, 4, '$2b$12$I9Zqd0yZMUrhP2LOMJ4szOmbTl3lzFl6cwW9HdiRC10IwGdZK8oma', '2025-06-05 09:06:17', '2025-06-06 09:06:17'),
(39, 4, '$2b$12$RWNnoSDaFd1L1YgwTZ72tO39UEO3ROie9gWM/ak5fS4E/C.5vUEXK', '2025-06-05 09:12:52', '2025-06-06 09:12:52'),
(42, 4, '$2b$12$d7JueWqiztKO0uo2wgHr8ur99ADDbxEWpFvszY.GY9y1xuyzuqVDe', '2025-06-05 09:35:20', '2025-06-06 09:35:20'),
(43, 4, '$2b$12$E/pOZ44gWqkz16XHMpiDf.W/Tkmfvb3kd5otwXE3SF38djEBxEOFO', '2025-06-05 09:45:29', '2025-06-06 09:45:29'),
(44, 4, '$2b$12$hr0Dm6GzeJDn.yl0PS8lE.KFsxH3D.9yt7rnrq6c73hWblby7RVzC', '2025-06-05 13:53:20', '2025-06-06 13:53:20'),
(45, 3, '$2b$12$CtKn1ymMzJPjf7VKIEzCjO1rU45VWH7b166BEdmnY459kqZuDcZ2u', '2025-06-06 11:22:44', '2025-06-07 11:22:44'),
(46, 4, '$2b$12$3FA4UC6tmy19Qv9OSUQnDeEuG7GJY1l5D7RDJwlW1.883Tj2ugB5G', '2025-06-06 11:23:21', '2025-06-07 11:23:21'),
(47, 5, '$2b$12$KCMbaj2KE3.BMNlbJtFMS.fFxE.TbzmtQmNPYKii1v0jReXZjMmqS', '2025-06-06 11:33:03', '2025-06-07 11:33:03'),
(48, 3, '$2b$12$mrM6xH0mTBc2WOz1oEKBQee5wMy2aVO7crseTx/ekn0WfcpXvfzBu', '2025-06-09 05:52:01', '2025-06-10 05:52:01'),
(49, 3, '$2b$12$DhoynTnttjk5fgeJWf4MxOVQlCaxZ8DD6O84XdZi29yLHu0Cynxae', '2025-06-09 05:53:28', '2025-06-10 05:53:28'),
(50, 4, '$2b$12$51LZgKY6nbz/cflW0SlETuBkPb8OxMIfkKvmsbY7AF1Npj70QEJTe', '2025-06-09 06:00:26', '2025-06-10 06:00:26'),
(51, 3, '$2b$12$8i2pE7DkawB3.8i.2Z697.ffcti4p.xr.HboJPP6sETC1z3vyu9hS', '2025-06-09 07:17:29', '2025-06-10 07:17:29'),
(52, 3, '$2b$12$.qk.keic4z9HTpzjjq7Er.S.O5gbbGxrTZHY4/RyLOS2nAuREwCzi', '2025-06-09 07:33:01', '2025-06-10 07:33:01'),
(54, 4, '$2b$12$vZx1SJWPXxojrTop6duNVOBjF72CRu1aKEzLaAyR3IVisnMyIoGMm', '2025-06-09 09:52:41', '2025-06-10 09:52:41'),
(55, 4, '$2b$12$wP1EIcFdUL.78ZthrSaFAeUqO62NYYXObffUKczYFZTV2NEHGfyse', '2025-06-09 09:57:57', '2025-06-10 09:57:57'),
(57, 3, '$2b$12$cTVEHiPVFAZD.btyoCsY4.H2QfzsNXy3HkzYNf7ZTz/D0j7hsTUVi', '2025-06-09 10:13:20', '2025-06-10 10:13:20'),
(60, 4, '$2b$12$c4.miQ2ID.5e0D4OpuB1pewq9pyhACQyvYMsFEAAH1pVTgINVbXpC', '2025-06-11 11:45:22', '2025-06-12 11:45:22'),
(61, 3, '$2b$12$lQ2fJp9Z9WmLvhPMXy2Im.j5.OGWnzrHyxA6z/Si5I45k.zip7Dra', '2025-06-11 11:46:35', '2025-06-12 11:46:35'),
(62, 3, '$2b$12$7AQ5C1YzLi19AlFo/O7eBODLBoqNfnQ2Pjpf2t1.CuQx7v8twZHiW', '2025-06-11 15:22:30', '2025-06-12 15:22:30'),
(69, 5, '$2b$12$G.V29lKZJztiNCoqj8.b2u8K.FRIpZGEuru8F3lpL87OGU54eZ9y6', '2025-06-11 17:54:32', '2025-06-12 17:54:32'),
(70, 3, '$2b$12$71YAQcPwhGSBVLO/oHWcaOb5aXObcHVekzF9ew1oYHaIPxXI2aZmO', '2025-06-12 03:27:22', '2025-06-13 03:27:22'),
(71, 3, '$2b$12$6WMWoaSOYXbA4Kj091CnLus.V.sYR4oI2eAMvzMcFCjtH8WrHEXvC', '2025-06-13 07:57:04', '2025-06-14 07:57:04'),
(72, 4, '$2b$12$1ggQ.fJkrVfNHbZylqN95e97j28jfv/enuwM7ePY9lgPHFDDtanUe', '2025-06-13 09:12:46', '2025-06-14 09:12:46'),
(73, 5, '$2b$12$7TwjAyTILfsJZRWEdISV9u5eH/dwFhw4fp1P8Z1MA54Tjsmknvequ', '2025-06-13 09:13:58', '2025-06-14 09:13:58'),
(74, 4, '$2b$12$VqN7ztnVkTAINK880BNIE.J.WGKmw1tCQLeM6k/K6hP8jtx6y8bnO', '2025-06-13 13:30:36', '2025-06-14 13:30:36'),
(75, 5, '$2b$12$WVwnuE1nJA6UX9uz95tIh.DUVT5gsLnz9ei82RaZr5bzkuxE/nJsG', '2025-06-13 14:15:38', '2025-06-14 14:15:38'),
(76, 3, '$2b$12$8hT2IPP3H0csyNUOSLT.XO8ZmDuC3eZDgIrbAOfZwR6lJVF4nTaWe', '2025-06-14 00:19:55', '2025-06-15 00:19:55'),
(78, 3, '$2b$12$nOvv6cpqFBYl0vTjdAlEQ.c3MgjFenbZQBOvxZwI9dMxw7buw/u1S', '2025-06-14 04:07:53', '2025-06-15 04:07:53'),
(79, 3, '$2b$12$HkzNd70n5ZYQ6XtIf4ifou0EAMHDfejDrkCTahazrqKGvLq5nxcj2', '2025-06-14 04:08:40', '2025-06-15 04:08:40'),
(81, 7, '$2b$12$cDVmV19iIsqvsPRtdZyIVuckEz7.Sjj6n6F7L2o8J2EwgEDQu3U1W', '2025-06-14 05:34:59', '2025-06-15 05:34:59'),
(82, 3, '$2b$12$.LDRDlWZe5I8tiQwTgbID.etJhVBnPnOIZo4H4pm5WaAnaXiQr0uq', '2025-06-14 11:31:11', '2025-06-15 11:31:11'),
(83, 3, '$2b$12$cgy5DRUFgJf8N2/wAnpmFedDk/rCZytlx0p9eQCNMfunRuf7ass3i', '2025-06-14 12:36:20', '2025-06-15 12:36:20');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `daftar_kelas`
--
ALTER TABLE `daftar_kelas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_matakuliah_id` (`matakuliah_id`),
  ADD KEY `fk_kelas_id` (`kelas_id`) USING BTREE;

--
-- Indexes for table `kelas`
--
ALTER TABLE `kelas`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mahasiswa`
--
ALTER TABLE `mahasiswa`
  ADD PRIMARY KEY (`id_mahasiswa`),
  ADD KEY `kelas_id` (`kelas_id`);

--
-- Indexes for table `matakuliah`
--
ALTER TABLE `matakuliah`
  ADD PRIMARY KEY (`id_mk`),
  ADD UNIQUE KEY `kode` (`kode`),
  ADD KEY `dosen_id` (`dosen_id`);

--
-- Indexes for table `presensi`
--
ALTER TABLE `presensi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `kelas_id` (`kelas_id`) USING BTREE,
  ADD KEY `fk_presensi_matakuliah` (`matakuliah_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `user_tokens`
--
ALTER TABLE `user_tokens`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `daftar_kelas`
--
ALTER TABLE `daftar_kelas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `kelas`
--
ALTER TABLE `kelas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `matakuliah`
--
ALTER TABLE `matakuliah`
  MODIFY `id_mk` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `presensi`
--
ALTER TABLE `presensi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=173;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `user_tokens`
--
ALTER TABLE `user_tokens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=84;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `daftar_kelas`
--
ALTER TABLE `daftar_kelas`
  ADD CONSTRAINT `fk_id_kelas` FOREIGN KEY (`kelas_id`) REFERENCES `kelas` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_matakuliah_id` FOREIGN KEY (`matakuliah_id`) REFERENCES `matakuliah` (`id_mk`) ON DELETE CASCADE;

--
-- Constraints for table `mahasiswa`
--
ALTER TABLE `mahasiswa`
  ADD CONSTRAINT `mahasiswa_ibfk_1` FOREIGN KEY (`kelas_id`) REFERENCES `kelas` (`id`);

--
-- Constraints for table `matakuliah`
--
ALTER TABLE `matakuliah`
  ADD CONSTRAINT `matakuliah_ibfk_1` FOREIGN KEY (`dosen_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `presensi`
--
ALTER TABLE `presensi`
  ADD CONSTRAINT `fk_presensi_matakuliah` FOREIGN KEY (`matakuliah_id`) REFERENCES `matakuliah` (`id_mk`) ON UPDATE CASCADE,
  ADD CONSTRAINT `presensi_ibfk_1` FOREIGN KEY (`kelas_id`) REFERENCES `kelas` (`id`);

--
-- Constraints for table `user_tokens`
--
ALTER TABLE `user_tokens`
  ADD CONSTRAINT `user_tokens_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
