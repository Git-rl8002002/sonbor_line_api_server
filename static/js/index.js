
function reload_uid_statistics2(val){
  
       let company = val;
        

        $.ajax({
                type:"POST",
                url:"/reload_uid_statistics2",
                data:{
                       'company':company 
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){

                        $('#show_menu_2').show(1000).html(res);
 
                },
                beforeSend:function(){
                        $('#status').html("reload LINE UID statistics  ...").css({'color':'blue'});
                },
                complete:function(){
                        $('#status').css({'color':'white'});
                }
        });
    
    }



function reload_uid_statistics(val){
  
        $.ajax({
                type:"POST",
                url:"/reload_uid_statistics",
                data:{
                        
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){

                        $('#show_menu_2').show(1000).html(res);
 
                },
                beforeSend:function(){
                        $('#status').html("reload LINE UID statistics  ...").css({'color':'blue'});
                },
                complete:function(){
                        $('#status').css({'color':'white'});
                }
        });
    
    }

    function del_uid_statistics2(val){
  
        let data    = val.split("/");
        let company = data[0];
        let id      = data[1];
        let uid     = data[2];
    
        // scroll to top 
        //jQuery("html,body").animate({scrollTop:0},1000);
    
        var check_del = prompt("刪除 " + company + " - " + id + " UID 確定刪除 , 再按一次 y ");
        
	if(check_del.toLowerCase() === 'y'){	
                $.ajax({
                        type:"POST",
                        url:"/del_uid_statistics",
                        data:{
                                'company':company,
                                'id':id,
                                'uid':uid
                        },
                        datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                                $('#click_show_msg').click();
                                $('#show_msg').show(1000).html(xhr.responseText);
                        },
                        success:function(res){
        
                                if(res == 'ok'){
                                        // show work detail by modal
                                        //$('#click_show_msg').click();
                                        //$('#show_msg').show(1000).html(res);

                                        alert(company + ' - ' + id + ' UID 刪除成功.');

                                        // reload UID statistics
                                        reload_uid_statistics2(company);
                                }
                                
                        },
                        beforeSend:function(){
                                $('#status').html("delete " + company + ' , ' + id + " UID  ...").css({'color':'blue'});
                        },
                        complete:function(){
                                $('#status').css({'color':'white'});
                        }
                });
        }

    
    }

function del_uid_statistics(val){
  
        let data    = val.split("/");
        let company = data[0];
        let id      = data[1];
        let uid     = data[2];
    
        // scroll to top 
        //jQuery("html,body").animate({scrollTop:0},1000);
    
        var check_del = prompt("刪除 " + company + " - " + id + " UID 確定刪除 , 再按一次 y ");
        
	if(check_del.toLowerCase() === 'y'){	
                $.ajax({
                        type:"POST",
                        url:"/del_uid_statistics",
                        data:{
                                'company':company,
                                'id':id,
                                'uid':uid
                        },
                        datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                                $('#click_show_msg').click();
                                $('#show_msg').show(1000).html(xhr.responseText);
                        },
                        success:function(res){
        
                                if(res == 'ok'){
                                        // show work detail by modal
                                        $('#click_show_msg').click();
                                        //$('#show_msg').show(1000).html(res);

                                        alert(company + ' - ' + id + ' UID 刪除成功.');

                                        // reload UID statistics
                                        reload_uid_statistics();
                                }
                                
                        },
                        beforeSend:function(){
                                $('#status').html("delete " + company + ' , ' + id + " UID  ...").css({'color':'blue'});
                        },
                        complete:function(){
                                $('#status').css({'color':'white'});
                        }
                });
        }

    
    }


function uid_statistics(val){
  
    let company = val;

    // scroll to top 
    jQuery("html,body").animate({scrollTop:0},1000);

    $.ajax({
            type:"POST",
            url:"/uid_statistics",
            data:{
                    'company':company
            },
            datatype:"html",
            error:function(xhr , ajaxError , throwError){
                    $('#click_show_msg').click();
                    $('#show_msg').show(1000).html(xhr.responseText);
            },
            success:function(res){
                    // show work detail by modal
                    $('#click_show_msg').click();
                    $('#show_msg').show(1000).html(res);
                    
            },
            beforeSend:function(){
                    $('#status').html("loading " + company + " UID 統計 ...").css({'color':'blue'});
            },
            complete:function(){
                    $('#status').css({'color':'white'});
            }
    });

}

function push_statistics3(val){
  
    let data = val.split('/');
    let company = data[0];
    let year    = data[1];
    let month   = data[2]; 

    //alert(comp);
   
    // scroll to top 
    //jQuery("html,body").animate({scrollTop:0},1000);

    $.ajax({
            type:"POST",
            url:"/push_statistics3",
            data:{
                    'company':company,
                    'year':year,
                    'month':month
            },
            datatype:"html",
            error:function(xhr , ajaxError , throwError){
                    $('#click_show_msg').click();
                    $('#show_msg').show(1000).html(xhr.responseText);
            },
            success:function(res){
                    // show work detail by modal
                    //$('#click_show_msg').click();
                    //$('#show_msg').show(1000).html(res);
                    
                    $('#show_detail_by_month').show(1000).html(res);


            },
            beforeSend:function(){
                    $('#status').html("loading " + company + " 推播記錄 ...").css({'color':'blue'});
            },
            complete:function(){
                    $('#status').css({'color':'white'});
            }
    });

}

function close_push_statistics3_1_list(){
        $('#show_detail_by_month2').hide(1000);
    }

function close_push_statistics3_list(){
    $('#show_detail_by_month').hide(1000);
}

function close_push_statistics2_1_list(){
        $('#show_detail_by_year2').hide(1000);
    }

function close_push_statistics2_list(){
    $('#show_detail_by_year').hide(1000);
}

function push_statistics3_1(val){
  
        let data = val.split('/');
        let company = data[0];
        let year    = data[1];
        let month   = data[2]; 
        let name    = data[3];
    
        // scroll to top 
        //jQuery("html,body").animate({scrollTop:0},1000);
    
        $.ajax({
                type:"POST",
                url:"/push_statistics3_1",
                data:{
                        'company':company,
                        'year':year,
                        'month':month,
                        'name':name
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        // show work detail by modal
                        //$('#click_show_msg').click();
                        //$('#show_msg').show(1000).html(res);
                        
                        $('#show_detail_by_month2').show(1000).html(res);
    
    
                },
                beforeSend:function(){
                        $('#status').html("loading " + company + " - " + year + " - " + name + " , 推播記錄 ...").css({'color':'blue'});
                },
                complete:function(){
                        $('#status').css({'color':'white'});
                }
        });
    
    }

function push_statistics2_1(val){
  
        let data = val.split('/');
        let company = data[0];
        let year    = data[1];
        let name    = data[2]; 
    
        //alert(val);
       
        // scroll to top 
        //jQuery("html,body").animate({scrollTop:0},1000);
    
        $.ajax({
                type:"POST",
                url:"/push_statistics2_1",
                data:{
                        'company':company,
                        'year':year,
                        'name':name
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        // show work detail by modal
                        //$('#click_show_msg').click();
                        //$('#show_msg').show(1000).html(res);
                        
                        $('#show_detail_by_year2').show(1000).html(res);
    
    
                },
                beforeSend:function(){
                        $('#status').html("loading " + company + " - " + year + " - " + name + " , 推播記錄 ...").css({'color':'blue'});
                },
                complete:function(){
                        $('#status').css({'color':'white'});
                }
        });
    
    }

function push_statistics2(val){
  
    let data = val.split('/');
    let company = data[0];
    let year    = data[1];
    let total   = data[2]; 

    //alert(comp);
   
    // scroll to top 
    //jQuery("html,body").animate({scrollTop:0},1000);

    $.ajax({
            type:"POST",
            url:"/push_statistics2",
            data:{
                    'company':company,
                    'year':year,
                    'total':total
            },
            datatype:"html",
            error:function(xhr , ajaxError , throwError){
                    $('#click_show_msg').click();
                    $('#show_msg').show(1000).html(xhr.responseText);
            },
            success:function(res){
                    // show work detail by modal
                    //$('#click_show_msg').click();
                    //$('#show_msg').show(1000).html(res);
                    
                    $('#show_detail_by_year').show(1000).html(res);


            },
            beforeSend:function(){
                    $('#status').html("loading " + company + " 推播記錄 ...").css({'color':'blue'});
            },
            complete:function(){
                    $('#status').css({'color':'white'});
            }
    });

}


function push_statistics(val){
  
    let company = val;

    // scroll to top 
    jQuery("html,body").animate({scrollTop:0},1000);

    $.ajax({
            type:"POST",
            url:"/push_statistics",
            data:{
                    'company':company
            },
            datatype:"html",
            error:function(xhr , ajaxError , throwError){
                    $('#click_show_msg').click();
                    $('#show_msg').show(1000).html(xhr.responseText);
            },
            success:function(res){
                    // show work detail by modal
                    $('#click_show_msg').click();
                    $('#show_msg').show(1000).html(res);

            },
            beforeSend:function(){
                    $('#status').html("loading " + company + " 推播記錄 ...").css({'color':'blue'});
            },
            complete:function(){
                    $('#status').css({'color':'white'});
            }
    });

}

function test(val){
   
    let data    = val.split('/');
    let company = data[0];
    let year    = data[1];
    let month   = data[2];

    $.ajax({
        type:"POST",
        url:"/test",
        data:{
                'company':company,
                'year':year,
                'month':month
        },
        datatype:"html",
        error:function(xhr , ajaxError , throwError){
                $('#click_show_msg').click();
                $('#show_msg').show(1000).html(xhr.responseText);
        },
        success:function(res){
                // show work detail by modal
             
                //$('#show_msg').show(1000).html(res);
                $('#show_detail').show(1000).html(res);


        },
        beforeSend:function(){
                $('#status').html("for test").css({'color':'blue'});
        },
        complete:function(){
                $('#status').css({'color':'white'});
        }
});
    

}

