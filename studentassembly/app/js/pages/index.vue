<template lang="jade">
v-header(header-class="header--landing")
section.page__wrapper
  .landing__wrapper
    //- .landing__overlay
    .landing__content
      h1 Fight corruption in your university.
      //- p Student Assembly empowers students to increase transparency and accountability on their schools.
      p Student Assembly is an anonymous reporting platform that aims to reduce corruption in universities.
      a.button(v-link="{ name: 'report' }") File a Report
      a.button.button--inverted(href="#how-it-works") Learn more
  .content__wrapper
    .content__section
      article.content__main
        h3 Latest reports
        v-report-list(v-bind:reports="reports" v-bind:loading="loading" v-bind:filters="false")
      aside.content__secondary
        h3 Top staff ratings
        .list__group
          a.list__item(
            v-for="person in staff"
          )
            h4
              span {{ person.name }}
              br
              small {{ person.school }}
            p {{ person.rating }} / 5

section.page__wrapper.page--light
  .content__wrapper
    .content__section
      .landing__hiw#how-it-works
        h2 How Student Assembly Works
        p.small Corruption the abuse of entrusted power for private gain. It occurs in universities because students aren’t empowered to report while schools want to keep their reputation. Student Assembly is designed to tackle this double barrier.
      .landing__features
        .landing__feature
          .landing__feature-icon
            img(src="/static/img/icons/action/ic_assignment_late_48px.svg" height="40")
          h3 Report
          p You deserve to be heard. Report quiet and hard corruption cases in your school and attach evidence via photos and documents.
        .landing__feature
          .landing__feature-icon
            img(src="/static/img/icons/action/ic_grade_48px.svg" height="40")
          h3 Rate
          p Inform others about underperformers and celebrate those who perform well! Rate the performance of your professors, school admins and staff.
        .landing__feature
          .landing__feature-icon
            img(src="/static/img/icons/action/ic_record_voice_over_48px.svg" height="40")
          h3 Amplify
          p Every problem is a community problem! Vote and share reports you like to get it more noticed. Subscribe to reports to get updates about its status.
        .landing__feature
          .landing__feature-icon
            img(src="/static/img/icons/action/ic_timeline_48px.svg" height="40")
          h3 Manage
          p School admins and student councils can manage and resolve reports. Help your school become more transparent, accountable and efficient!
v-footer
</template>

<script>
import Header from '../components/header.vue'
import Footer from '../components/footer.vue'
import ReportList from '../components/report-list.vue'

export default {
  data () {
    return {
      reports: [],
      loading: true,
      staff: [
        {
          name: 'Juan dela Cruz',
          school: 'PUP Manila',
          rating: 3
        },
        {
          name: 'Juana dela Cruz',
          school: 'UP Diliman',
          rating: 3
        }
      ]
    }
  },
  created () {
    this.$http.get('report?limit=5').then(
      function(response) {
        this.reports = response.data
        this.loading = false
      },
      function(response) {
        console.log('Failed to retrieve published reports.')
      }
    )
  },
  components: {
    'v-header': Header,
    'v-footer': Footer,
    'v-report-list': ReportList
  }
}
</script>
