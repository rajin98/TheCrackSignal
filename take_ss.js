function takeSS(){
   var prevA = document.querySelector('#selenium-download-link');
   if(prevA) prevA.remove();
   var video = document.querySelector('video');
   var canvas = document.createElement('canvas');
   var context = canvas.getContext('2d');
   var ratio, myHeight, myWidth;

   ratio = video.videoWidth/video.videoHeight;
   myWidth = video.videoWidth-100;
   myHeight = parseInt(myWidth/ratio,10);
   canvas.width = myWidth;
   canvas.height = myHeight;

   context.fillRect(0,0,myWidth,myHeight);
   context.drawImage(video,0,0,myWidth,myHeight);

   var dl = document.createElement('a');
   dl.href = canvas.toDataURL("image/jpeg");
   dl.target = '_blank';
   dl.id = 'selenium-download-link'
   dl.download = 'ss.jpg';
   document.body.appendChild(dl)
}

takeSS();