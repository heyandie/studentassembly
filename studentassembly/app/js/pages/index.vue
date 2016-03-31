<template lang="jade">
v-header(header-class="header--landing")
section.page__wrapper.page--landing
  .landing__wrapper
    .landing__overlay
    .landing__content
      h1 Fight corruption at your university.
      //- p Student Assembly empowers students to increase transparency and accountability on their schools.
      p Student Assembly is an anonymous reporting platform that aims to reduce corruption in universities.
      a.button.button--inverted(v-link="{ name: 'report' }") File a Report
  .content__wrapper
    .content__section
      p Corruption the abuse of entrusted power for private gain. It occurs in universities because students aren’t empowered to report while schools want to keep their reputation. Student Assembly is designed to tackle this double barrier.
      .landing__features#how-it-works
        .landing__feature
          img(src="/static/img/icons/action/ic_assignment_late_48px.svg")
          h2 Report
          p You deserve to be heard. Report quiet and hard corruption cases in your school and attach evidence via photos and documents.
        //- .landing__feature
        //-   img(src="/static/img/icons/action/ic_search_48px.svg")
        //-   h2 Search
        //-   p You can’t protect yourself from what you don’t know. Browse existing reports and ratings using various filters.
        .landing__feature
          img(src="/static/img/icons/action/ic_grade_48px.svg")
          h2 Rate
          p Inform others about underperformers and celebrate those who perform well! Rate the performance of your professors, school admins and staff.
        .landing__feature
          img(src="/static/img/icons/action/ic_record_voice_over_48px.svg")
          h2 Amplify
          p Every problem is a community problem! Vote and share reports you like to get it more noticed. Subscribe to reports to get updates about its status.
        .landing__feature
          img(src="/static/img/icons/action/ic_timeline_48px.svg")
          h2 Manage
          p School admins and student councils can manage and resolve reports. Help your school become more transparent, accountable and efficient!

</template>

<script>
import Header from '../components/header.vue'
import Footer from '../components/footer.vue'

export default {
  components: {
    'v-header': Header,
    'v-footer': Footer
  }
}
</script>
