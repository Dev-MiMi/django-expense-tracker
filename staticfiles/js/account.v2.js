// small helper: close button goes back one page
document.addEventListener('DOMContentLoaded', function(){
  const close = document.getElementById('closeBtn');
  if (close) close.addEventListener('click', function(e){
    e.preventDefault();
    if (document.referrer) {
      window.history.back();
    } else {
      // fallback: hide card
      document.querySelector('.card').style.display = 'none';
    }
  });
});
