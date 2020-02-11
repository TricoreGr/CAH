<template>
      <v-app>
        <navbar/>
        <div class="about">
            <div class="about__wrapper">
            <h1 class="about__title">made with LOVE by...</h1>
            <div class="about__images-wrapper">
                        <aboutContainer v-for="(user, index) in users" :key="index" :link="user.link" :information="user.information" :name="user.name" :images="user.images">
                        </aboutContainer>
            </div>
            <h1 class="about__title">big thanks to...</h1>
            <div class="about__images-wrapper">
                        <aboutContainer v-for="(teacher, index) in teachers" :key="index"  :name="teacher.name" :link="teacher.link" :information="teacher.information" :images="teacher.images">
                        </aboutContainer>
            </div>
            </div>
        </div>
      </v-app>
</template>

<script>
import anime from "animejs/lib/anime.es.js";
import aboutContainer from "../components/aboutContainer"
import jojos0 from '../images/jojos0.jpg'
import jojos1 from '../images/jojos1.jpg'
import tolis0 from '../images/tolis0.jpg'
import tolis1 from '../images/tolis1.jpg'
import giapa0 from '../images/giapa0.jpg'
import giapa1 from '../images/giapa1.jpg'
import stoug0 from '../images/stoug0.jpg'
import stoug1 from '../images/stoug1.jpg'
import asidirop0 from '../images/asidirop0.jpg'
import asidirop1 from '../images/asidirop1.jpg'

export default {
    components: { aboutContainer},
  name: "About",
  data() {
    return {
        users:[
            {
                name:'Georgios "Atlas" Apostolopoulos',
                information:"Project manager - Full stack developer - Dev ops engineer - Coffee drinking machine - Beard cultivator",
                images:[
          jojos0,
          jojos1  
        ],
        link:"https://gitlab.com/joj0s"
        },
        {
                name:'Gregory "The bad merger" Giapa',
                information:"Back end developer - Database administrator - Drunk committer - Testing allergic - Beer devourer",
                images:[
          giapa0,
          giapa1  
        ],
        link:"https://github.com/Giapa"
        },
        {
                name:'Apostolos "Front-End machine" Kalovelo',
                information:"Front end developer - UI/UX Designer - Executive Creative Director - Potential weeaboo - Harry Potter copy",
                images:[
          tolis0,
          tolis1],
          link:"https://kalovelo.com"}
        ],
        teachers:[
            {
                name:'Stefanos "Stoug" Ougiaroglou',
                information:"Ivan Savvidis' bodyguard",
                images:[
          stoug0,
          stoug1  
        ],link:"https://aetos.it.teithe.gr/~stoug/index.html",
        },
        {
                name:'Antonis "Asidirop" Sidiropoulos',
                information:"Php artisan",
                images:[
          asidirop0,
          asidirop1  
        ],link:"https://people.iee.ihu.gr/~asidirop/hp/",
        }
        ]
    }
  },
  methods:{
      hoverAnimation(){
          var canChangePhoto = true;
          anime({
              targets:'.about__image',
              duration:150,
              opacity:[1,0],
              complete:()=>{
                  anime({
              targets:'.about__image',
              duration:150,
              opacity:[0,1],
              update:(anim)=>{
                  if(Math.round(anim.progress)>20 && canChangePhoto)
                  {this.isHovered=!this.isHovered;
                  canChangePhoto=false}
              }
              })
              }
      })
  },
  getHoverStatus(){
      return this.isHovered? this.images[1]:this.images[0]
  }
  }
};
</script>
