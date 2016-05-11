<template lang="jade">
section.page__wrapper
  .landing__hero
    //- .landing__overlay
    .landing__content
      h1 Fight corruption in your university.
      p Student Assembly is where you can anonymously report corruption cases in your university. We’ll ensure your anonymity and help resolve the problem at the same time.
      a.button(v-link="{ name: 'report' }") File a Report
      a.button.button--inverted(href="#how-it-works") Learn more
  .content__wrapper
    .content__section
      article.content__main
        h3 Latest reports
        v-report-list(:reports="reports", :loading="loading", :filters="false")
          template(slot="list_empty")
            img.list__empty-icon(src="/static/img/icons/action/ic_assignment_48px.svg")
            p.small Start by filing a corruption report. You can also look for existing reports by using the search bar on the topmost area of the page.
            a.button.button--small(v-link="{ name: 'file-a-report' }") File a report

      aside.content__secondary
        h3 Top staff ratings
        .u-mg-t-24(v-for="member in staff")
          a(v-link="{ name: 'rate-view', params: { 'id': member.id } }")
            h5 {{ member.name }}
            p.small
              span {{ member.school | truncate 36 }}
              br
              strong {{ member.votes || 'No' }} {{ member.votes | pluralize 'rating' }}
              span(v-if="member.votes") &nbsp;&mdash; overall: {{ member.rating.overall }}

section.page__wrapper.page--light
  .content__wrapper
    .content__section
      .landing__hiw#how-it-works
        h2 How Student Assembly Works
        p.small Corruption is the abuse of entrusted power for private gain. It occurs in universities because students aren’t empowered to report while schools want to keep their reputation. Student Assembly tackles this double barrier by providing students with an anonymous reporting platform and giving universities an efficient report management tool.
      .landing__features
        .landing__feature
          .landing__feature-icon
            img(src="/static/img/icons/action/ic_assignment_late_48px.svg", height="40")
          h3 Report
          p You deserve to be heard. Report quiet and hard corruption cases in your school and attach evidence via photos, audio/visual recordings or documents.
        .landing__feature
          .landing__feature-icon
            img(src="/static/img/icons/action/ic_grade_48px.svg", height="40")
          h3 Rate
          p Inform others about underperformers and celebrate those who perform well! Rate the performance of your professors, school administration and staff.
        .landing__feature
          .landing__feature-icon
            img(src="/static/img/icons/action/ic_record_voice_over_48px.svg", height="40")
          h3 Amplify
          p Every problem is a community problem! Vote and share reports you like to get it more noticed. Subscribe to reports to get updates about its status.
        .landing__feature
          .landing__feature-icon
            img(src="/static/img/icons/action/ic_timeline_48px.svg", height="40")
          h3 Manage
          p School admins and student councils can manage and resolve reports. Help your school become more transparent, accountable and efficient!

section.page__wrapper.page--bg-cubes
  .content__wrapper
    .content__section
      .landing__cta
        h1 You deserve to be heard.
        p Start using Student Assembly now!
        a.button(v-link="{ name: 'report' }") File a Report

</template>

<script>
import ReportList from '../components/report-list.vue'

export default {
  data () {
    return {
      reports: [],
      staff: [],
      loading: true,
    }
  },
  created () {
    this.$http.get('report?limit=5').then(
      function(response) {
        this.reports = response.data.reports
        this.loading = false
      },
      function(response) {
        console.log('Failed to retrieve published reports.')
      }
    )

    this.$http.get('staff?top=True&limit=5').then(
      (response) => {
        this.staff = response.data
      },
      (response) => {
        console.log('Failed to retrieve staff members.')
      }
    )
  },
  components: {
    'v-report-list': ReportList
  }
}
</script>
