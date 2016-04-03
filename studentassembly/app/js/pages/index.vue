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
        .list__group
          a.list__item(
            v-for="report in reports"
            v-link="{ name: 'report-view', params: { id: report.id } }"
          )
            h4
              .pull-right
                small.list__item-remark(:class="report.is_approved ? 'list__item--approved' : 'list__item--not-approved'")
                  | {{ report.is_approved ? 'Resolved' : 'Unresolved' }}
              span {{ report.category }}
              br
              small {{ report.school }}
            p.small {{ report.updated_at | relativeDate }}
            p {{ report.text | truncate }}
      aside.content__secondary
        h3 Top staff ratings

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
        //- .landing__feature
        //-   img(src="/static/img/icons/action/ic_search_48px.svg" height="40")
        //-   h2 Search
        //-   p You can’t protect yourself from what you don’t know. Browse existing reports and ratings using various filters.
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

</template>

<script>
import RelativeDate from 'relative-date'

import Header from '../components/header.vue'
import Footer from '../components/footer.vue'

export default {
  data () {
    return {
      reports: []
    }
  },
  created () {
    this.$http.get('report?limit=5').then(
      function(response) {
        this.reports = response.data
      },
      function(response) {
        console.log('Failed to retrieve published reports.')
      }
    )
  },
  filters: {
    truncate (string) {
      if (string.length > 140)
        return string.substring(0, 140) + '...'
      else
        return string
    },
    count (arr) {
      this.$set('filteredLength', arr.length)
      return arr
    },
    relativeDate (date) {
      return RelativeDate(Date.parse(date))
    }
  },
  components: {
    'v-header': Header,
    'v-footer': Footer
  }
}
</script>
