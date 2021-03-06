SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE  TABLE IF NOT EXISTS `vindula_myvindulaDB`.`vin_comissao_usuario` (
  `id` INT(10) NOT NULL AUTO_INCREMENT ,
  `ci` VARCHAR(10) NOT NULL ,
  `cpf` VARCHAR(15) NOT NULL ,
  `pv_bonus` INT(10) NOT NULL DEFAULT 0 ,
  `pv_mensal` INT(10) NOT NULL DEFAULT 0 ,
  `pv_total` DECIMAL(10,2) NOT NULL DEFAULT 0.0 ,
  `pv_meta` VARCHAR(45) NOT NULL DEFAULT 0 ,
  `valor_inicial` DECIMAL(10,2) NOT NULL DEFAULT 0.0 ,
  `me_meta` TINYINT(1) NOT NULL DEFAULT FALSE ,
  `me_porcentagem` INT(10) NOT NULL DEFAULT 0 ,
  `equipe` VARCHAR(45) NOT NULL ,
  `valor_final` DECIMAL(10,2) NOT NULL DEFAULT 0.0 ,
  `competencia` VARCHAR(45) NOT NULL ,
  `sequencia` INT(10) NOT NULL DEFAULT 0 ,
  `faltas` INT(10) NOT NULL DEFAULT 0 ,
  `atrasos` INT(10) NOT NULL DEFAULT 0 ,
  `adicional1` DECIMAL(10,2) NOT NULL DEFAULT 0.0 ,
  `head_shot` INT(10) NOT NULL DEFAULT 0 ,
  `adicional2` DECIMAL(10,2) NOT NULL DEFAULT 0.0 ,
  `bv_porcentagem` INT(10) NOT NULL DEFAULT 0 ,
  `adicional3` DECIMAL(10,2) NOT NULL DEFAULT 0.0 ,
  `q_proposta` INT(10) NOT NULL DEFAULT 0 ,
  `media_dia` INT(10) NOT NULL DEFAULT 0 ,
  `adicional4` DECIMAL(10,2) NOT NULL DEFAULT 0.0 ,
  `ticket` INT(10) NOT NULL DEFAULT 0 ,
  `adicional5` DECIMAL(10,2) NOT NULL DEFAULT 0.0 ,
  `date_created` DATETIME NOT NULL ,
  `date_modified` DATETIME NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1

CREATE  TABLE IF NOT EXISTS `vindula_myvindulaDB`.`vin_comissao_venda` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `sequencia` INT(10) NOT NULL DEFAULT 0 ,
  `ci_usuario` VARCHAR(10) NOT NULL ,
  `competencia` VARCHAR(45) NOT NULL ,
  `nome_cliente` VARCHAR(200) NOT NULL ,
  `cpf` VARCHAR(15) NOT NULL ,
  `data_atd` DATE NOT NULL ,
  `situacao` VARCHAR(200) NULL ,
  `situacao_financeiro` VARCHAR(200) NULL ,
  `status` TINYINT(1) NOT NULL DEFAULT FALSE ,
  `pontos` INT(10) NOT NULL DEFAULT 0 ,
  `date_created` DATETIME NOT NULL ,
  `date_modified` DATETIME NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1

CREATE  TABLE IF NOT EXISTS `vindula_myvindulaDB`.`vin_comissao_validacao` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `username` VARCHAR(45) NOT NULL ,
  `cpf` VARCHAR(15) NOT NULL ,
  `competencia` VARCHAR(45) NOT NULL ,
  `sequencia_venda` INT(11) NOT NULL ,
  `sequencia_usuario` INT(11) NOT NULL ,
  `date_created` DATETIME NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1
COLLATE = latin1_swedish_ci;

 
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
