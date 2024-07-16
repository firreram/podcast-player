document.querySelector('#textsearch').addEventListener('click', e =>{
    e.preventDefault();
    
    let user_input = document.querySelector('#searchbar');
    const targets = document.querySelectorAll('.searchtarget');
    for (let target of targets) {
      target.classList.remove('hide');
      let content = target.innerHTML.toLowerCase();
      if (content.search(user_input.value.toLowerCase()) != -1){
      }
      else {
        target.classList.add('hide');
      }
    }
  })
