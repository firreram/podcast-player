links=document.querySelectorAll('.category-filter');

for (let l0 of links){
    if (l0.dataset.option === 'Tutte'){
      l0.classList.add('fw-bold');  //add default higlight to 'Tutte' link
      }
    }

  links.forEach(link => {
    link.addEventListener('click', e => {
      e.preventDefault();
      
      const filter = e.target.dataset.option;
      for (let l of links){
        l.classList.remove('fw-bold');  //remove highlight for all links in advance
      }

      if(filter === 'Tutte'){
        link.classList.add('fw-bold');
      }
      else if(filter === 'Politica'){
        link.classList.add('fw-bold');
      }
      else if(filter === 'Musica'){
        link.classList.add('fw-bold');
      }
      else if(filter === 'Scienze'){
        link.classList.add('fw-bold');
      }
      else if(filter === 'Varie'){
        link.classList.add('fw-bold');
      }

      const series = document.querySelectorAll('.serie'); //!!!add class selector for series 
      for (let serie of series) {
          serie.classList.remove('hide');  //remove hide for all series in advance
           
        if(filter === 'Tutte'){
        }
        else if (filter === 'Politica' && serie.dataset.category===filter){
        }
        else if (filter === 'Musica' && serie.dataset.category===filter){
        }
        else if (filter === 'Scienze' && serie.dataset.category===filter){
        }
        else if (filter === 'Varie' && serie.dataset.category===filter){
        }
        else{
          serie.classList.add('hide');
        }
          
      }
    });
  });