$j(document).ready(function(){
	var common_content_filter = '#content=*,dl.portalMessage.error,dl.portalMessage.info';
	var common_jqt_config = {fixed:false,speed:'fast',mask:{color:'#000',opacity: 0.4,loadSpeed:0,closeSpeed:0}};
	
    $j('a.validacao').prepOverlay({
        subtype: 'ajax',
        noform:'reload',
        filter: common_content_filter,
        closeselector: '[name=form.cancel]',
        formselector: '[name=comisao-form]',
        width: '50%',
        config: common_jqt_config,

    });

    var max_colspan = 0
    $j('.cal_colspan').each(function(){
    	var valor = $j(this).attr('data-cont');
    	if (valor > max_colspan){
    		max_colspan = valor;
    	}
    });
    $j('.cal_colspan').each(function(){
    	var valor = $j(this).attr('data-cont'),
    		last = $j(this).attr('data-last');
		if ((max_colspan%valor)==0){
			$j(this).attr('colspan', max_colspan/valor );
		}else{
			if (last == "True"){
				$j(this).attr('colspan', (max_colspan % valor) + 1 );
			}else{
				$j(this).attr('colspan', max_colspan % valor );
			}

		}
	});

	$j('#table_adicionais tr th').attr('colspan',parseInt(max_colspan)+3)


});