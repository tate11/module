  function hideMarkDescription(id){
    document.getElementById(id).style.display = "none";
  };

  function showMarkDescription(mark_id, des_id){
    var des_top = parseInt(document.getElementById(mark_id).offsetTop, 10) - 145 + 'px';
    var des_left = parseInt(document.getElementById(mark_id).offsetLeft, 10) - 228 + 'px' ;
    document.getElementById(des_id).style.display = "block";
    document.getElementById(des_id).style.top = des_top;
    document.getElementById(des_id).style.left = des_left;
  };

