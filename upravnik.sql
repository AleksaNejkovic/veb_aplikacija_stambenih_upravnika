-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Nov 16, 2020 at 11:51 PM
-- Server version: 8.0.18
-- PHP Version: 7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `upravnik`
--

DELIMITER $$
--
-- Functions
--
DROP FUNCTION IF EXISTS `vrstaUloge`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `vrstaUloge` (`id_uloga` INT(11)) RETURNS VARCHAR(200) CHARSET utf8 BEGIN
	DECLARE vrsta_uloge varchar(200);
		SELECT uloga INTO vrsta_uloge FROM uloga WHERE id_uloga = id;
	RETURN vrsta_uloge;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `korisnici`
--

DROP TABLE IF EXISTS `korisnici`;
CREATE TABLE IF NOT EXISTS `korisnici` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ime` varchar(200) NOT NULL,
  `prezime` varchar(200) NOT NULL,
  `broj_telefona` varchar(200) NOT NULL,
  `korisnicko_ime` varchar(200) NOT NULL,
  `korisnicka_lozinka` varchar(200) NOT NULL,
  `uloga` int(11) NOT NULL,
  `broj_stana` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_uloga` (`uloga`)
) ENGINE=InnoDB AUTO_INCREMENT=143 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `korisnici`
--

INSERT INTO `korisnici` (`id`, `ime`, `prezime`, `broj_telefona`, `korisnicko_ime`, `korisnicka_lozinka`, `uloga`, `broj_stana`) VALUES
(1, 'Aleksa', 'Nejković', '0600326267', 'admin', 'admin', 3, '16'),
(90, 'Bojan', 'Stojanović', '060213125', 'bojan.stojanovic.1', 'pbkdf2:sha256:150000$BZZI7BRZ$5d2abdc0095ba59c33dafa2640bc60b72a4a812ea3b8f558af8b251d456e753c', 2, '1'),
(91, 'Vera', 'Stojanović', '060213125', 'vera.stojanovic.1', 'pbkdf2:sha256:150000$LufvwRQp$72b84edfe0b45a9e49d59f3a1cc396c7fe4dc138bbe124af9293d2a01db7c526', 2, '1'),
(92, 'Vera', 'Alilković', '0633115611', 'vera.alilkovic.2', 'pbkdf2:sha256:150000$8SgAlW5F$4e22434b8203bf91a6177e1eed5162494b5d103da9af3b1a95cf9938f650e24e', 2, '2'),
(93, 'Aleksandar', 'Alilković', '063123151', 'aleksandar.alilkovic.2', 'pbkdf2:sha256:150000$4M7ZulBX$27df9ae087d79a6d1eec7f77c3935d0fbff9721a77f174bd059a231ccb2d39a7', 2, '2'),
(94, 'Ana', 'Stojadinović', '06221465', 'ana.stojadinovic.3', 'pbkdf2:sha256:150000$qdG3HYTI$e4ce0f804097a0128609a4d13f6f20b876135b0ae17dc57ad62d12c2a7f31c4c', 2, '3'),
(95, 'Nebojša', 'Stojadinović', '065543252', 'nebojsa.stojadinovic.3', 'pbkdf2:sha256:150000$2b6DRbyG$bbc31547b35ff3d0cd17c1784db1171fa6de9ec593e52fa38e5f7796ef7407be', 2, '3'),
(96, 'Miloš', 'Stojadinović', '061324561', 'milos.stojadinovic.3', 'pbkdf2:sha256:150000$PkTBK9fM$7b2b8f7388b86055e97dc35851587c329f86aba16cd588b4d56f77d4e6d77b9d', 2, '3'),
(97, 'Daniela', 'Stojadinović', '0631122456', 'daniela.stojadinovic.3', 'pbkdf2:sha256:150000$XRCCqFpK$343bb54b451a27c8629d860c397aaa23233e29aa48f7a25782d2d3827366de04', 2, '3'),
(98, 'Slobodan', 'Milić', '064111466', 'slobodan.milic.4', 'pbkdf2:sha256:150000$EvfCuYKP$5a47f6edbad2bb79ac9c75d300746aa3c354b74a325b1f77d094c4aa87f71f6e', 2, '4'),
(99, 'Katarina', 'Milić', '061224551', 'katarina.milic.4', 'pbkdf2:sha256:150000$xPveOdu3$22923417b3a4ea05cdf019eff5b1f5469a94dfbdbaa52bfa651aa5720f0062b7', 2, '4'),
(100, 'Hristina', 'Milić', '061123455', 'hristina.milic.4', 'pbkdf2:sha256:150000$V8BqFH5k$2cd61c05cd18a747b579a5d0a804599d7ed3b278fb29ce7a4b9f04799ff2e560', 2, '4'),
(101, 'Anđelija', 'Milić', '067787678', 'andjelija.milic.4', 'pbkdf2:sha256:150000$DBFRZELE$63ce28983dbfc52bf09a95712299667646912f6695ace8375cd293aacc7c68b2', 2, '4'),
(102, 'Dejan', 'Filipović', '061223466', 'dejan.filipović.5', 'pbkdf2:sha256:150000$qt5sQiIr$ff61c38e123c325d6d5ccef9e9dedd304c14ce16d81d031a4c562551bfe6b3eb', 2, '5'),
(103, 'Ninoslav', 'Mladenović', '06124125125', 'ninoslav.mladenovic.6', 'pbkdf2:sha256:150000$O1E1Auwt$15f4f4004338fce1ea64027859f181d58d6bc037c651d010d364d24a75a153a3', 2, '6'),
(104, 'Mira', 'Mladenović', '062941481', 'mira.mladenovic.6', 'pbkdf2:sha256:150000$VbxXfbsD$99202df91605dfafeb260ac3c54d12419574c18af0ea42be632914b1a90b8865', 2, '6'),
(105, 'Snežana', 'Džekov', '0627872898', 'snezana.dzekov.7', 'pbkdf2:sha256:150000$y4De17pa$84a0dae8fd442958828b3fa6054d8bb816bde1fadb4536ed5458922fe88a98fd', 2, '7'),
(106, 'Miodrag', 'Miltenov', '061234441', 'miodrag.miltenov.9', 'pbkdf2:sha256:150000$8yrAgO0r$57907e4bbdea3ce6c32aa0571a1158be54b986b2fb96efdf989df5925d22a27f', 2, '9'),
(107, 'Dragica', 'Miltenov', '062111235', 'dragica.miltenov.9', 'pbkdf2:sha256:150000$NprCWy6N$504c436e76b4eacc1f56f4acc9777831916ce8850f89a89154cadcf55805b1c0', 2, '9'),
(108, 'Dalibor', 'Petrović', '068822141', 'dalibor.petrovic.10', 'pbkdf2:sha256:150000$3hOhnU45$b0a41696b8b6faab5f4a0d397be6c9f9c2dd83cf7179c08113a2e0537b7000d6', 2, '10'),
(109, 'Dobrinka', 'Petrović', '0612411212', 'dobrinka.petrovic.10', 'pbkdf2:sha256:150000$HCE5AmV4$ff1edbbd8633c7f44d24d43517f2ebd8c787311f25e49da495c5b401bfe614d3', 2, '10'),
(110, 'Daniela', 'Petrović', '06244441111', 'daniela.petrovic.10', 'pbkdf2:sha256:150000$xI6cCYR5$7748c98f743c9eeb315a77759a0eedebd5388adf2ad9a18fb74d821acf4730aa', 2, '10'),
(111, 'Rodoljub', 'Nešić', '062727281', 'rodoljub.nesic.11', 'pbkdf2:sha256:150000$5y4PrWT3$1047099cdd657a5775b83d3fc94a2201522fc3ef68dc8da606225c88c450f6ae', 2, '11'),
(112, 'Milica', 'Nešić', '062214551', 'milica.nesic.11', 'pbkdf2:sha256:150000$E7iXHAE7$68ad0d35778075e29858a9303aa0ac969e11de2e2866953a930c2a7c64f46253', 2, '11'),
(113, 'Jovana', 'Nešić', '062155122', 'jovana.nesic.11', 'pbkdf2:sha256:150000$oGejJzJb$1535e879d62445fe188db72876bdb603d84af3fd7a6b3790a7d28f66b8e99e55', 2, '11'),
(114, 'Anđela', 'Nešić', '060023545', 'andjela.nesic.11', 'pbkdf2:sha256:150000$5sBBM5Bn$ea7541bf1299aa3ec039510a5af3ee9168b20181379e0027e5c81dd9a7b43d02', 2, '11'),
(115, 'Nikolina', 'Nešić', '061234455', 'nikolina.nesic.11', 'pbkdf2:sha256:150000$ELbRFiSN$c171f9211392875a30fb2113664f04635872417bb857f220a406df71f841961a', 2, '11'),
(116, 'Rade', 'Bošković', '060987987', 'rade.boskovic.12', 'pbkdf2:sha256:150000$ziJgx2n9$b7cd4b8c46a7878872008952775e8932f2c4f2ca6a5682dfe3f12be85a63cb3e', 2, '12'),
(117, 'Vladan', 'Zlatković', '065656422', 'vladan.zlatkovic.13', 'pbkdf2:sha256:150000$R6PjCGcl$a8d14865ca3ab5e46b908f66ca5eccfa6a349773f48cb6fd551b1bf6cc927fe2', 2, '13'),
(118, 'Sonja', 'Zlatković', '06232415', 'sonja.zlatković.13', 'pbkdf2:sha256:150000$kCXtooXp$8d00319e1df8be2ce223f9d1ab8d0eb706714a0e0277f9cd9655d2e78e96531b', 2, '13'),
(119, 'Anka', 'Nedelkov', '0621251212', 'anka.nedelkov.14', 'pbkdf2:sha256:150000$UGnUGKWF$f7d28b8c7b88b74471566db280f57f02323d101fa185fadc53044db6ddc65cab', 2, '14'),
(120, 'Olivera', 'Nejković', '0601536100', 'olivera.nejkovic.16', 'pbkdf2:sha256:150000$I8lgjpvv$656470f5a9452fa01a0876d1e09616cff955273009983e9873997ed98b21a1c3', 2, '16'),
(121, 'Dušica', 'Đorđević', '062255111', 'dusica.djordjevic.17', 'pbkdf2:sha256:150000$jDyd3iL3$83f0e1c544425ddd78174cd57bab3444d713246697d34e8c935ccd2dc9a7c0ce', 2, '17'),
(122, 'Ivan', 'Đorđević', '061245122', 'ivan.djordjevic.18', 'pbkdf2:sha256:150000$3bHdceV0$dcb311e4de9746a273cb7dc26ed809e9cb8863f4aa6fbaa41b2dd9e13dfa8bed', 2, '18'),
(123, 'Dušanka', 'Đorđević', '062125122', 'dusanka.djordjevic.18', 'pbkdf2:sha256:150000$hcxKgk5A$6075870f97fe541da331dc4b00aea34e8a084e162bb67ff04ae263b06ef30e77', 2, '18'),
(124, 'Vukan', 'Đorđević', '0611245112', 'vukan.djordjevic.18', 'pbkdf2:sha256:150000$uzDpdkpr$ab9e9f1731dad67803e2c15d4b21970bc2b59592a67fbccd6c7d3453874e7b65', 2, '18'),
(125, 'Miomir', 'Miladinović', '0622151512', 'miomir.miladinovic.19', 'pbkdf2:sha256:150000$0rDg1qaP$d2a3fe00049c13b205de53da33a285e4fc9b3d2171751c31b3d8be701e6ecfef', 2, '19'),
(126, 'Mira', 'Miladinović', '0612412152', 'mira.miladinovic.19', 'pbkdf2:sha256:150000$AoEUJRxG$02b1d3848d09dab2520994b091c53c87e0812f1aa637d210f04e0613f1ce54b7', 2, '19'),
(127, 'Aleksandar', 'Nešić', '0678899224', 'aleksandar.nesic.20', 'pbkdf2:sha256:150000$IFwGuqgw$38cba56766a700c8dddc3fd1f7a3d9e913fa49439b1791c967f6bedd799d3218', 2, '20'),
(128, 'Zoran', 'Stamenović', '065225222', 'zoran.stamenovic.21', 'pbkdf2:sha256:150000$JsvDfdbh$bc72bb056c2bb13ee35f12736a97f8207387ef4ac92ab296332341996801836c', 2, '21'),
(129, 'Milos', 'Stamenović', '062251512', 'milos.stamenovic.21', 'pbkdf2:sha256:150000$5J5eICys$5f03cc607a9a33a428eb99ff633e404b890377088a35a666db856c346ac16f20', 2, '21'),
(130, 'Jovanka', 'Stamenović', '062324551', 'jovanka.stamenovic.21', 'pbkdf2:sha256:150000$2wu7PJtf$f1d1f546618422432b5b90574fa581dd199b5a23045666f7ee4319eff207cdd9', 2, '21'),
(131, 'Milica', 'Stamenović', '065428162', 'milica.stamenovic.21', 'pbkdf2:sha256:150000$iOBhBQuS$ec2bbc59bb269382ba29d327573eb11211cc7e6583450e64a9756ba5225f5e7b', 2, '21'),
(132, 'Rade', 'Stamenović', '067225111', 'rade.stamenovic.21', 'pbkdf2:sha256:150000$J0dEg3Yj$0b72a8816b3196b7978ce2fdad060826340b7e2c0f04b3ccc09359151fc85a49', 2, '21'),
(133, 'Dragan', 'Đorđević', '0622151525', 'dragan.djordjevic.22', 'pbkdf2:sha256:150000$ugaWTepG$0d78f0e741226b48bd16fb0a2c2fdbc46546fa513ee1ea7c0524deff5c4e6663', 2, '22'),
(134, 'Daniela', 'Đorđević', '06451212', 'daniela.djordjevic.22', 'pbkdf2:sha256:150000$w0hQzXoa$d62f7f41322109a998e825a6ed37874224feb640ceb2eee42009c211425068ae', 2, '22'),
(135, 'Mila', 'Đorđević', '064123412', 'mila.djordjevic.22', 'pbkdf2:sha256:150000$9Ly3amkx$9c2b2b05b7d4f59763adf41720aa73f2062878804b813ba2d617fb45390c4c9f', 2, '22'),
(136, 'Miodrag', 'Mladenović', '061241256', 'miodrag.mladenovic.23', 'pbkdf2:sha256:150000$4O9YqN2k$a6ed9b1bacf7f2286af91c265bb705d8369a3b6b2971d2031027f5a2b89d4ac9', 2, '23'),
(137, 'Olivera', 'Mladenović', '063125122', 'olivera.mladenovic.23', 'pbkdf2:sha256:150000$RxL29Mnh$7a8ab97b2bba92d047895c9d446d9e3b97aa36521e3d1dc8e6858f2c6ae4dcdc', 2, '23'),
(138, 'Igor', 'Dimitrov', '061212124', 'igor.dimitrov.24', 'pbkdf2:sha256:150000$OTe4WKlV$0d9a0b3a15364ab291f9b44d98dbcdf6a73f663200a54b45eb8de630b28002a7', 2, '24'),
(139, 'Slađana', 'Dimitrov', '0612412512', 'sladjana.dimitrov.24', 'pbkdf2:sha256:150000$FK1j8Jqn$7d4dbc7ee348d30e0c984048a60470bd969a17d80cf29e458698da500a372c0a', 2, '24'),
(140, 'Emil', 'Dimitrov', '0614126122', 'emil.dimitrov.24', 'pbkdf2:sha256:150000$DCcVxP6g$5daa645fbcacca852453ab5de3d0e17c635efe593b16dd9f819132a3f870e2cf', 2, '24'),
(141, 'Bogdan', 'Mladenović', '0612412512', 'bogdan.mladenovic.6', 'pbkdf2:sha256:150000$2piE6dTa$8c3c7cf435b2eec0bffef6504b666f043fbd2b5b42d624dcce0797e3b92a8d86', 2, '6'),
(142, 'Jovan', 'Nejković', '0600326267', 'jovan.nejkovic.16', 'pbkdf2:sha256:150000$rkxXFmxH$6695ce987b01cb9185c9ee1c31d9c431463bdc695c9069cdec4520403e4a103f', 1, '16');

-- --------------------------------------------------------

--
-- Table structure for table `obavestenja`
--

DROP TABLE IF EXISTS `obavestenja`;
CREATE TABLE IF NOT EXISTS `obavestenja` (
  `id_obavestenja` int(11) NOT NULL AUTO_INCREMENT,
  `posiljalac` varchar(200) NOT NULL,
  `broj_posiljaoca` varchar(200) NOT NULL,
  `primalac` varchar(200) NOT NULL,
  `broj_primaoca` varchar(200) NOT NULL,
  `datum` varchar(200) NOT NULL,
  `vreme` varchar(200) NOT NULL,
  `sadrzaj` varchar(1000) NOT NULL,
  PRIMARY KEY (`id_obavestenja`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `obavestenja`
--

INSERT INTO `obavestenja` (`id_obavestenja`, `posiljalac`, `broj_posiljaoca`, `primalac`, `broj_primaoca`, `datum`, `vreme`, `sadrzaj`) VALUES
(22, 'Olivera Nejković', '0601536100', 'Jovan Nejković', '0600326267', '27/10/2020', '23:33:34', 'sada'),
(25, 'Jovan Nejković', '0600326267', 'Olivera Nejković', '0601536100', '28/10/2020', '18:53:07', 'Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! Dugačak tekst! ');

-- --------------------------------------------------------

--
-- Table structure for table `placeni_racuni_cistac`
--

DROP TABLE IF EXISTS `placeni_racuni_cistac`;
CREATE TABLE IF NOT EXISTS `placeni_racuni_cistac` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datum` varchar(200) NOT NULL,
  `vreme` varchar(200) NOT NULL,
  `broj_racuna` varchar(200) NOT NULL,
  `iznos` varchar(200) NOT NULL,
  `mesec_vazenja` varchar(200) NOT NULL,
  `broj_stana` varchar(200) NOT NULL,
  `korisnicko_ime` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `placeni_racuni_cistac`
--

INSERT INTO `placeni_racuni_cistac` (`id`, `datum`, `vreme`, `broj_racuna`, `iznos`, `mesec_vazenja`, `broj_stana`, `korisnicko_ime`) VALUES
(1, '03/11/2020', '19:28:07', '111', '6683.33', 'oktobar', '16', 'olivera.nejkovic.16');

-- --------------------------------------------------------

--
-- Table structure for table `placeni_racuni_fond`
--

DROP TABLE IF EXISTS `placeni_racuni_fond`;
CREATE TABLE IF NOT EXISTS `placeni_racuni_fond` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datum` varchar(200) NOT NULL,
  `vreme` varchar(200) NOT NULL,
  `broj_racuna` varchar(200) NOT NULL,
  `iznos` varchar(200) NOT NULL,
  `mesec_vazenja` varchar(200) NOT NULL,
  `broj_stana` varchar(200) NOT NULL,
  `korisnicko_ime` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `placeni_racuni_fond`
--

INSERT INTO `placeni_racuni_fond` (`id`, `datum`, `vreme`, `broj_racuna`, `iznos`, `mesec_vazenja`, `broj_stana`, `korisnicko_ime`) VALUES
(1, '03/11/2020', '21:01:42', '1711', '6925.94', 'oktobar', '16', 'olivera.nejkovic.16'),
(2, '03/11/2020', '22:02:20', '1233', '8586.39', 'septembar', '16', 'olivera.nejkovic.16');

-- --------------------------------------------------------

--
-- Table structure for table `placeni_racuni_struja`
--

DROP TABLE IF EXISTS `placeni_racuni_struja`;
CREATE TABLE IF NOT EXISTS `placeni_racuni_struja` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datum` varchar(200) NOT NULL,
  `vreme` varchar(200) NOT NULL,
  `broj_racuna` varchar(200) NOT NULL,
  `iznos` varchar(200) NOT NULL,
  `mesec_vazenja` varchar(200) NOT NULL,
  `broj_stana` varchar(200) NOT NULL,
  `korisnicko_ime` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `placeni_racuni_struja`
--

INSERT INTO `placeni_racuni_struja` (`id`, `datum`, `vreme`, `broj_racuna`, `iznos`, `mesec_vazenja`, `broj_stana`, `korisnicko_ime`) VALUES
(7, '03/11/2020', '00:54:30', '1231', '6000.00', 'oktobar', '16', 'olivera.nejkovic.16'),
(8, '17/11/2020', '00:41:43', '7877', '30000.00', 'septembar', '16', 'olivera.nejkovic.16');

-- --------------------------------------------------------

--
-- Table structure for table `placeni_racuni_voda`
--

DROP TABLE IF EXISTS `placeni_racuni_voda`;
CREATE TABLE IF NOT EXISTS `placeni_racuni_voda` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datum` varchar(200) NOT NULL,
  `vreme` varchar(200) NOT NULL,
  `broj_racuna` varchar(200) NOT NULL,
  `iznos` varchar(200) NOT NULL,
  `mesec_vazenja` varchar(200) NOT NULL,
  `broj_stana` varchar(200) NOT NULL,
  `korisnicko_ime` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `placeni_racuni_voda`
--

INSERT INTO `placeni_racuni_voda` (`id`, `datum`, `vreme`, `broj_racuna`, `iznos`, `mesec_vazenja`, `broj_stana`, `korisnicko_ime`) VALUES
(1, '03/11/2020', '19:01:50', '1444', '6987.67', 'oktobar', '16', 'olivera.nejkovic.16');

-- --------------------------------------------------------

--
-- Table structure for table `racuni_cistac`
--

DROP TABLE IF EXISTS `racuni_cistac`;
CREATE TABLE IF NOT EXISTS `racuni_cistac` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `broj_racuna` varchar(200) NOT NULL,
  `mesec_vazenja` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `iznos` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `racuni_cistac`
--

INSERT INTO `racuni_cistac` (`id`, `broj_racuna`, `mesec_vazenja`, `iznos`) VALUES
(2, '111', 'oktobar', '120300'),
(3, '1245', 'novembar', '137000'),
(4, '1567', 'decembar', '125555');

-- --------------------------------------------------------

--
-- Table structure for table `racuni_fond`
--

DROP TABLE IF EXISTS `racuni_fond`;
CREATE TABLE IF NOT EXISTS `racuni_fond` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `broj_racuna` varchar(200) NOT NULL,
  `mesec_vazenja` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `iznos` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `racuni_fond`
--

INSERT INTO `racuni_fond` (`id`, `broj_racuna`, `mesec_vazenja`, `iznos`) VALUES
(3, '1233', 'septembar', '154555'),
(4, '1711', 'oktobar', '124667'),
(5, '1833', 'novembar', '122344');

-- --------------------------------------------------------

--
-- Table structure for table `racuni_struja`
--

DROP TABLE IF EXISTS `racuni_struja`;
CREATE TABLE IF NOT EXISTS `racuni_struja` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `broj_racuna` varchar(200) NOT NULL,
  `mesec_vazenja` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `iznos` varchar(200) NOT NULL,
  `utroseno_kwh` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `racuni_struja`
--

INSERT INTO `racuni_struja` (`id`, `broj_racuna`, `mesec_vazenja`, `iznos`, `utroseno_kwh`) VALUES
(7, '7877', 'septembar', '540000', '568'),
(8, '1231', 'oktobar', '108000', '223'),
(9, '12312', 'novembar', '225555', '225');

-- --------------------------------------------------------

--
-- Table structure for table `racuni_voda`
--

DROP TABLE IF EXISTS `racuni_voda`;
CREATE TABLE IF NOT EXISTS `racuni_voda` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `broj_racuna` varchar(200) NOT NULL,
  `mesec_vazenja` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `iznos` varchar(200) NOT NULL,
  `utroseno_m3` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `racuni_voda`
--

INSERT INTO `racuni_voda` (`id`, `broj_racuna`, `mesec_vazenja`, `iznos`, `utroseno_m3`) VALUES
(5, '8778', 'septembar', '143000', '455'),
(6, '1444', 'oktobar', '125778', '114'),
(7, '7777', 'novembar', '165434', '866');

-- --------------------------------------------------------

--
-- Table structure for table `uloga`
--

DROP TABLE IF EXISTS `uloga`;
CREATE TABLE IF NOT EXISTS `uloga` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uloga` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `uloga`
--

INSERT INTO `uloga` (`id`, `uloga`) VALUES
(1, 'upravnik'),
(2, 'stanar'),
(3, 'admin');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `korisnici`
--
ALTER TABLE `korisnici`
  ADD CONSTRAINT `fk_uloga` FOREIGN KEY (`uloga`) REFERENCES `uloga` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
