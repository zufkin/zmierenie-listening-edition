const key='zmierenie-ch04-scroll';
const saved=Number(localStorage.getItem(key)||0);
if(saved>0&&saved<document.body.scrollHeight){requestAnimationFrame(()=>scrollTo({top:saved,behavior:'auto'}));}
let timer;
addEventListener('scroll',()=>{clearTimeout(timer);timer=setTimeout(()=>localStorage.setItem(key,String(scrollY)),250);},{passive:true});
addEventListener('beforeunload',()=>localStorage.setItem(key,String(scrollY)));
