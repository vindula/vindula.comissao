
ALTER TABLE `vindula_myvindulaDB`.`vin_comissao_venda` ADD COLUMN `nr_proposta` VARCHAR(45) NOT NULL  AFTER `ci_usuario` ,  ADD COLUMN `deleted` TINYINT(1) NULL DEFAULT FALSE  AFTER `aprovado`, ADD INDEX `venda_idx` (`ci_usuario` ASC, `nr_proposta` ASC, `competencia` ASC) ;

ALTER TABLE `vindula_myvindulaDB`.`vin_comissao_validacao` CHANGE COLUMN `sequencia_venda` `id_venda` INT(11) NOT NULL  , CHANGE COLUMN `sequencia_usuario` `id_usuario` INT(11) NOT NULL  ;

ALTER TABLE `vindula_myvindulaDB`.`vin_comissao_usuario`   DROP COLUMN `adicional5` , DROP COLUMN `ticket` , DROP COLUMN `adicional4` , DROP COLUMN `media_dia` , DROP COLUMN `q_proposta` , DROP COLUMN `adicional3` , DROP COLUMN `bv_porcentagem` , DROP COLUMN `adicional2` , DROP COLUMN `head_shot` , DROP COLUMN `adicional1` , DROP COLUMN `atrasos` , DROP COLUMN `faltas` , CHANGE COLUMN `pv_total` `pv_total` DECIMAL(10,2) NOT NULL DEFAULT 0.0  , CHANGE COLUMN `valor_inicial` `valor_inicial` DECIMAL(10,2) NOT NULL DEFAULT 0.0  , CHANGE COLUMN `valor_final` `valor_final` DECIMAL(10,2) NOT NULL DEFAULT 0.0  ;

ALTER TABLE `vindula_myvindulaDB`.`vin_comissao_usuario` ADD COLUMN `deleted` TINYINT(1)  NOT NULL DEFAULT FALSE AFTER `name`;


CREATE  TABLE IF NOT EXISTS `vindula_myvindulaDB`.`vin_comissao_adicional` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(45) NOT NULL ,
  `direito` TINYINT(1) NOT NULL DEFAULT Flase ,
  `valor` DECIMAL(10,2) NOT NULL ,
  `dict_itens` VARCHAR(45) NOT NULL ,
  `id_usuario` INT(10) NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1
COLLATE = latin1_swedish_ci;