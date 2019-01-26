$(function(){
    var checkbox=$( 'input[id=high]' );
    
    if( sessionStorage[ 'show' ] == 'ok' ){  $("li.off").show();checkbox[0].checked=true }
        
    checkbox.click( function(){

        if(  this.checked ){ 
            sessionStorage[ 'show' ]='ok'
            $("li.high").fadeIn('slow');
        } else {
            sessionStorage[ 'show' ]='no'
            $("li.high").fadeOut('slow');
        }
    
})
    
    })

$(function(){
    var checkbox=$( 'input[id=mid]' );
    
    if( sessionStorage[ 'show' ] == 'ok' ){  $("li.mid").show();checkbox[0].checked=true }
        
    checkbox.click( function(){

        if(  this.checked ){ 
            sessionStorage[ 'hided' ]='ok'
            $("li.mid").fadeIn('slow');
        } else {
            sessionStorage[ 'hided' ]='no'
            $("li.mid").fadeOut('slow');

        }
    
})
    
    })
    
$(function(){
    var checkbox=$( 'input[id=low]' );
    
    if( sessionStorage[ 'show' ] == 'ok' ){  $("li.mek").show();checkbox[0].checked=true }
        
    checkbox.click( function(){

        if(  this.checked ){ 
            sessionStorage[ 'show' ]='ok'
            $("li.low").fadeIn('slow');
        } else {
            sessionStorage[ 'show' ]='no'
            $("li.low").fadeOut('slow');
        }
    
})
    
    })