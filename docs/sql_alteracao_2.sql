
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
