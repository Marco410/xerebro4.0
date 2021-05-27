    var loading = document.getElementById('contenedor_load');
    var pagina_completa = document.getElementById('pagina_completa');
    loading.style.visibility = 'hidden';

    function ConfigInicial(id,idA){
        const url = "get-config/"+id+"/"+idA;
        if(id == 0 && idA == 0){
            //se igualan a 0 al momento que no tiene configuracion activa
            iziToast.info({
                timeout:3000,
                id:'info',
                theme:'dark',
                color:'black',
                title:'Alerta',
                position:'center',//topRight
                message:'Selecciona una configuración'
            });
            $('#modalConf').modal('show');
        }else{
            fetch(url).then(response => response.json()).then(function(data){
                if(data.v){           
                 canales = data.canales.split(",");
                 canales.pop();
                 var j = 1
                 var k = 1
                 if($(".ch")){
                     $(".ch").remove();
                 }
                     for(i = 0; i <= canales.length; i++){
                         
                         if(i > 6 && i < 13){
                             
                         $("#cb"+j+"").append("<p class='ch'><label><input data-name='"+canales[i-1]+"' name='canal[]' type='checkbox' value='ch"+i+"' onclick='validar()' /> "+canales[i-1]+"</label></p>");
                         j++;
                 
                         }else if(i > 12){
                             
                             $("#cb"+k+"").append("<p class='ch'><label><input data-name='"+canales[i-1]+"' name='canal[]' type='checkbox' value='ch"+i+"' onclick='validar()' /> "+canales[i-1]+"</label></p>");
                             k++;
                     
                         }
                         else  {
                         $("#cb"+i+"").append("<p class='ch'><label><input data-name='"+canales[i-1]+"' name='canal[]' type='checkbox' value='ch"+i+"' onclick='validar()' /> "+canales[i-1]+"</label></p>");
                         }

                         $("#NCanales").val(i);
                     }
                     document.getElementById("idConf").value = ""+ id;
                     
                     return iziToast.success({
                        timeout:3000,
                        id:'info',
                        title:'Éxito',
                        position:'center',//topRight
                        message:'Configuración instalada'
                    });
                     
                 }else{
                    return iziToast.error({
                        timeout:3000,
                        id:'info',
                        title:'Error',
                        position:'center',//topRight
                        message:'Selecciona una configuración valida'
                    });
                 }
             });
        }
    }

    $('#main-table').DataTable({
        searching:false,
        lengthMenu:[[5,10,15,-1],[5,10,15,"Todos"]],
        scrollX: true,
        scrollCollapse:true,
		columnDefs: [{
            orderable: false,
            targets:   0
        }
		],
		language: {
			"sProcessing":     "Procesando...",
			"sLengthMenu":     "Mostrar _MENU_ registros",
			"sZeroRecords":    "No se encontraron resultados",
			"sEmptyTable":     "Ningún dato disponible en esta tabla",
			"sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
			"sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
			"sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
			"sInfoPostFix":    "",
			"sSearch":         "Buscar:",
			"sUrl":            "",
			"sInfoThousands":  ",",
			"sLoadingRecords": "Cargando...",
			"oPaginate": {
				"sFirst":    "Primero",
				"sLast":     "Último",
				"sNext":     "Siguiente",
				"sPrevious": "Anterior"
			},
			"oAria": {
				"sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
				"sSortDescending": ": Activar para ordenar la columna de manera descendente"
			}
		},
		dom: '<"row" <"col-sm-4" l> <"col-sm-8" <"pull-right ml-15" B><"pull-right" f> > >r<"mt-30" t><"row mt-30" <"col-sm-5" i> <"col-sm-7" p> >',
		buttons: [
		{
			extend: 'excel',
			className: 'btn btn-success',
			exportOptions: {
				columns: ':not(:last-child)',
			},
			init: function(api, node, config) {
				$(node).removeClass('dt-button');
			}
		},
		{
			text: 'Guarda Tabla',
			className: 'btn btn-primary',
			action: function(e, dt, node, config){
				window.location.href = base_url + 'pedidos/nuevo'
			},
			init: function(api, node, config) {
				$(node).removeClass('dt-button');
			}
		}
		],
    });


    $(".btn-get-config").click(function(){
        $('#modalConf').modal('hide');
        id = $(this).attr("data-id");
        name = $(this).attr("data-name");
        document.getElementById("name-conf").innerHTML = name;
        idA = document.getElementById("idA").value;

        ConfigInicial(id,idA);
        
        document.getElementById("idA").value= id;
       
        
    });

    idGlobal = document.getElementById("idConf").value;
    idA = document.getElementById("idA").value;
    ConfigInicial(idGlobal,idA);
    
    $( "#condicion" ).change(function() {
        if($(this).val() != ""){
        var fd = new FormData();
        var fm = document.getElementById("fm_user").value;
        

        csrftoken = getCookie('csrftoken');
        fd.append("csrfmiddlewaretoken",csrftoken);
        fd.append("fm_user",fm);
        fd.append("condicion",$(this).val());
        loading.style.visibility = 'visible';
        pagina_completa.className += " opacidad";

        const response = axios.post('/tabla',fd).then(res =>  {
            
                if(response){
                    
                    document.getElementById("btn-excel").hidden = false;
                    document.getElementById("tabla_res").innerHTML = res.data;
                    iziToast.info({
                        timeout: 2000,
                        title: 'Tabla',
                        position: 'topRight',
                        message: 'Correcta. Mostrando...',
                        theme:'light',
                        color:'white',
                    });
                    console.log("Cargando");  

                }else{
                    iziToast.error({
                        timeout: 3000,
                        title: 'Error',
                        position: 'topRight',
                        message: 'No se pudo obtener la tabla.',
                    });
            }
    
        }).catch((err) => {
            iziToast.error({
                timeout: 6000,
                title: 'Error',
                position: 'topRight',
                message: 'Algo salio mal, intentelo de nuevo y recargue.',
            });
        }).then(function() {
            loading.style.visibility = 'hidden';
            pagina_completa.className -= " opacidad";
            console.log("Termino");
          });
    }
      });

    $("#btn-add-ch").click(function(){
        var no = document.getElementById("no_canales").value;
        var j = 1
        var k = 1
        if($(".ch")){
            $(".ch").remove();
        }
            for(i = 1; i <= no; i++){

                if(no <= 12){
                    if(i == 1 || i == 2 ){
                        $("#qcb1").append("<p class='ch'><label> CH"+i+" <input tabindex='"+i+"' class='form-control' name='ch[]' type='text' placeholder='-' value='' required /></label></p>");
                    }
                    else if (i == 3 || i == 4){
                        $("#qcb2").append("<p class='ch'><label> CH"+i+" <input tabindex='"+i+"' class='form-control' name='ch[]' type='text' placeholder='-' value='' required /></label></p>");
                    }
                    else if (i == 5 || i == 6){
                        $("#qcb3").append("<p class='ch'><label> CH"+i+" <input tabindex='"+i+"' class='form-control' name='ch[]' type='text' placeholder='-' value='' required /></label></p>");
                    } 
                    else if (i == 7 || i == 8){
                        $("#qcb4").append("<p class='ch'><label> CH"+i+" <input tabindex='"+i+"' class='form-control' name='ch[]' type='text' placeholder='-' value='' required /></label></p>");
                    } 
                    else if (i == 9 || i == 10){
                        $("#qcb5").append("<p class='ch'><label> CH"+i+" <input tabindex='"+i+"' class='form-control' name='ch[]' type='text' placeholder='-' value='' required /></label></p>");
                    }
                    else if (i == 11 || i == 12){
                        $("#qcb6").append("<p class='ch'><label> CH"+i+" <input tabindex='"+i+"' class='form-control' name='ch[]' type='text' placeholder='-' value='' required /></label></p>");
                    } 
                }else{
                    if(i == 1 || i == 2 || i == 3 ){
                        $("#qcb1").append("<p class='ch'><label> CH"+i+" <input tabindex='"+i+"' class='form-control' name='ch[]' type='text' placeholder='-' value='' required /></label></p>");
                    }
                    else if (i == 4 || i == 5 || i == 6  ){
                        $("#qcb2").append("<p class='ch'><label> CH"+i+" <input tabindex='"+i+"' class='form-control' name='ch[]' type='text' placeholder='-' value='' required /></label></p>");
                    }
                    else if (i == 7 || i == 8 || i == 9){
                        $("#qcb3").append("<p class='ch'><label> CH"+i+" <input tabindex='"+i+"' class='form-control' name='ch[]' type='text' placeholder='-' value='' required /></label></p>");
                    } 
                    else if (i == 10 || i == 11 || i == 12){
                        $("#qcb4").append("<p class='ch'><label> CH"+i+" <input tabindex='"+i+"' class='form-control' name='ch[]' type='text' placeholder='-' value='' required /></label></p>");
                    } 
                    else if (i == 13 || i == 14 || i == 15){
                        $("#qcb5").append("<p class='ch'><label> CH"+i+" <input tabindex='"+i+"' class='form-control' name='ch[]' type='text' placeholder='-' value='' required /></label></p>");
                    }
                    else if (i == 16 || i == 17 || i == 18){
                        $("#qcb6").append("<p class='ch'><label> CH"+i+" <input tabindex='"+i+"' class='form-control' name='ch[]' type='text' placeholder='-' value='' required /></label></p>");
                    } 
                }
               
                
              
            }
    
    });

    $('#btn-new-conf').click(function(){
        $('#card-new-conf').show();

    });

$("#btn-clean").click(function(){
    $(".ch").remove();
});

$("#btn-save-par").click(function(){
        var canales = [];

        $("input[name='canal[]']").each(function(indice, elemento) {
            
            if($(elemento).is(':checked')){
                canales.push($(elemento).attr("data-name"));
            }else{
                
            }
      });

      if (canales.length == 2){
         
        var form = document.getElementById("form-graficar");
        var fd = new FormData(form);
        csrftoken = getCookie('csrftoken');
        fd.append("csrfmiddlewaretoken",csrftoken);      
        const response = axios.post('/cor',fd).then(res =>  {
    
                if(response){
                    iziToast.info({
                        timeout: 3000,
                        title: 'Valores ',
                        position: 'topRight',
                        message: 'Calculados Correctamente',
                        theme:'light',
                        color:'green',
                    });
                      
                var t = $('#main-table').DataTable();
                var v = 1;
                t.row.add([
                    canales,
                    res.data.correlacion[0],res.data.coherencia[0],res.data.correlacion[1], res.data.coherencia[1],res.data.correlacion[2],res.data.coherencia[2],res.data.correlacion[3],res.data.coherencia[3],res.data.correlacion[4],res.data.coherencia[4],"<a class='btn btn-danger btn-sm'><i class='fa fa-times' style='color:white' ></i></a>"
                ]).draw(false);
        

                }else{
                    iziToast.error({
                        timeout: 3000,
                        title: 'Error',
                        position: 'topRight',
                        message: 'No se pudo gráficar.',
                    });
            }
    
        }).catch((err) => {
            iziToast.error({
                timeout: 6000,
                title: 'Error',
                position: 'topRight',
                message: 'Algo salio mal, intentelo de nuevo y recargue.',
            });
        });
         
      
    
    }else{
        iziToast.warning({
            timeout: 4000,
            title:"¡Cuidado!",
            message:"Selecciona solo solo dos canales para comparar",
            position:'center'
        }); 
      }
     
});

/*
$('#form-insert-config').validate({

    submitHandler: function(form) {
        $.ajax({
            url: '/save-config',
            type:  'post',
            data: $(form).serialize(),
            success: function(respuesta){
                var res = JSON.stringify(respuesta);
                console.log("REs"+res);
                if(res.name != ""){
                        Cookies.set('message', { type: 'info', message: 'Configuración Guardada'+res.name});
                        window.location.href = "/";
                }else{
                    iziToast.error({
                        timeout: 3000,
                        title: 'Error',
                        position: 'topRight',
                        message: 'No se pudo guardar.',
                    });
                }
            },
            error:  function(xhr,err){ 
                console.log("readyState: "+xhr.readyState+"\nstatus: "+xhr.status+"\n \n responseText: "+xhr.responseText);
            }
        });
    }
});
*/
$('#btn-insert-conf').click(async()=>{
    var form = document.getElementById("form-insert-config");
    var fd = new FormData(form);
    csrftoken = getCookie('csrftoken');
    fd.append("csrfmiddlewaretoken",csrftoken);      
    const response = axios.post('/save-config',fd,).then(res =>  {
        
        if(response){
            if (res.name == ""){
                iziToast.error({
                    timeout: 3000,
                    title: 'Error',
                    position: 'center',
                    message: 'Da un nombre a tu configuración. ',
                });
            }else{
                Cookies.set('message', { type: 'info', message: 'Configuración Guardada'+res.name});
                window.location.href = "/";
            }
            
        }
       

    }).catch((err) => {
        iziToast.error({
            timeout: 4000,
            title: 'Error',
            position: 'center',
            message: 'Te falto llenar un campo o el archivo no tiene el formato correcto. Verifique. ',
        });
    });
    

});



$('#btn-graficar-senal').click(async()=>{
        var form = document.getElementById("form-graficar");
        var fd = new FormData(form);
        csrftoken = getCookie('csrftoken');
        fd.append("csrfmiddlewaretoken",csrftoken);      
        const response = await axios.post('/upload_csv',fd,{
            onUploadProgress(e){
                var progress = (e.loaded*100) / e.total;
                var element = document.getElementById('file-upload');
                element.style.width= progress+"%";
            }
        }).then(res =>  {

                if(res.data.name != ""){
                    document.getElementById("img-senal").src = '/static/core/senales/'+ res.data.name;
                    iziToast.info({
                        timeout: 3000,
                        title: 'Grafica',
                        position: 'topRight',
                        message: 'Correcta',
                        theme:'light',
                        color:'white',
                    });
                }else{
                    iziToast.error({
                        timeout: 3000,
                        title: 'Error',
                        position: 'topRight',
                        message: 'No se pudo gráficar.',
                    });
            }

        }).catch((err) => {
            iziToast.error({
                timeout: 6000,
                title: 'Error',
                position: 'topRight',
                message: 'Algo salio mal, intentelo de nuevo y recargue.',
            });
        });
        

});

$('#btn-graficar-pc').click(async()=>{
    var form = document.getElementById("form-analisis");
    var fd = new FormData(form);
    var fm = document.getElementById("fm_user").value;
    var file_name = document.getElementById("file").value;
    csrftoken = getCookie('csrftoken');
    fd.append("csrfmiddlewaretoken",csrftoken);
    var values = $("input[name='canal[]']").map(function(){ if($(this).prop('checked')){return $(this).val()}   }).get();
    fd.append("file_name",$('input[type=file]')[0].files[0]);
    fd.append("canal[]",values);
    fd.append("fm_user",fm);
            
    const response = await axios.post('/pds',fd,{
        onUploadProgress(e){
            var progress = (e.loaded*100) / e.total;
            var element = document.getElementById('file-upload');
            element.style.width= progress+"%";
        }
    }).then(res =>  {
            if(res.data.name != ""){
                document.getElementById("img-senal").src = '/static/core/senales/'+ res.data.name;
                iziToast.info({
                    timeout: 3000,
                    title: 'Grafica',
                    position: 'topRight',
                    message: 'Correcta',
                    theme:'light',
                    color:'white',
                });
            }else{
                iziToast.error({
                    timeout: 3000,
                    title: 'Error',
                    position: 'topRight',
                    message: 'No se pudo gráficar.',
                });
        }

    }).catch((err) => {
        iziToast.error({
            timeout: 6000,
            title: 'Error',
            position: 'topRight',
            message: 'Algo salio mal, intentelo de nuevo y recargue.',
        });
    });
    

});

function validar(){
    
    console.log("Click");
    var canales = [];

        $("input[name='canal[]']").each(function(indice, elemento) {
            
            if($(elemento).is(':checked')){
                canales.push($(elemento).attr("data-name"));
            }else{
                $(elemento).removeAttr('checked');
            }
      });

      if (canales.length > 2){
        iziToast.warning({
            timeout: 3500,
            title:"¡Cuidado!",
            message:"Selecciona solo dos canales para comparar.",
            position:'center'
        }); 
      }

}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

