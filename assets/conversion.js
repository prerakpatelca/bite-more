/* Progressive menu search and device-aware app CTA. No automatic redirects. */
(function(){
 'use strict';
 var apple='https://apps.apple.com/us/app/bite-more/id6801191446';
 var android='https://play.google.com/store/apps/details?id=com.storefrontconsumer.bite.more&hl=en_US';
 document.querySelectorAll('.bm-device-link').forEach(function(a){
  if(/Android/i.test(navigator.userAgent)){a.href=android;a.textContent='Get the Android App';}
  else if(/iPhone|iPad|iPod/i.test(navigator.userAgent)){a.href=apple;a.textContent='Get the iPhone App';}
  else{a.href='#';a.textContent='Choose your app store above';a.addEventListener('click',function(e){e.preventDefault();document.querySelector('.store-badge').focus();});}
 });
 var input=document.getElementById('menu-search');
 if(input){
  document.getElementById('menu-search-controls').hidden=false;
  var items=Array.from(document.querySelectorAll('.carta .item'));
  var status=document.getElementById('menu-search-status');
  input.addEventListener('input',function(){
   var q=input.value.trim().toLocaleLowerCase();var count=0;
   items.forEach(function(el){var show=!q||el.textContent.toLocaleLowerCase().includes(q);el.hidden=!show;if(show)count++;});
   document.querySelectorAll('.carta').forEach(function(list){
    var empty=!Array.from(list.querySelectorAll('.item')).some(function(el){return !el.hidden;});list.hidden=empty;
    var note=list.previousElementSibling;var heading=note&&note.previousElementSibling;
    if(note&&note.classList.contains('cat-note'))note.hidden=empty;
    if(heading&&heading.classList.contains('cat-title'))heading.hidden=empty;
   });
   status.textContent=q?(count?count+' matching dishes':'No dishes found. Try pasta, chicken or wings.'):'Browse all '+items.length+' dishes.';
  });
  status.textContent='Browse all '+items.length+' dishes.';
  document.querySelectorAll('.bm-category-nav a').forEach(function(a){a.addEventListener('click',function(){if(input.value){input.value='';input.dispatchEvent(new Event('input'));}});});
 }
 document.addEventListener('click',function(e){var a=e.target.closest('a[href]');if(!a||!window.bmTrack)return;
  var href=a.getAttribute('href');
  if(href.includes('apps.apple.com')||href.includes('play.google.com'))window.bmTrack('app_download_click',{platform:href.includes('apps.apple.com')?'ios':'android',placement:a.closest('.bm-app-promo')?'homepage':a.closest('header')?'navigation':'app_page'});
  else if(/(?:^|\/)(buckhead|duluth)(?:\.html)?$/.test(href)&&!/^https?:/.test(href))window.bmTrack('location_view_click',{location:href.includes('duluth')?'duluth':'buckhead'});
 });
})();
