<template lang="jade">
v-header(header-class="header--landing")
section.page__wrapper.page--landing
  .landing__wrapper
    .landing__overlay
    .landing__content
      h1
        | You deserve to be heard.
      p Student Assembly empowers students to increase transparency and accountability on their schools.
      a.button.button--inverted(v-link="{ name: 'report' }") File a Report
  .content__wrapper
    .content__section
      .landing__features#how-it-works
        .landing__feature
          img(src="/static/img/icons/action/ic_assignment_late_48px.svg")
          h2 Report
          p Report administrators, teachers, and schools for corrupt policies and practices anonymously.
        .landing__feature
          img(src="/static/img/icons/action/ic_timeline_48px.svg")
          h2 Analyze
          p School administrators can manage reports by tagging them as resolved, dismissed, and in-progress.
        .landing__feature
          img(src="/static/img/icons/action/ic_grade_48px.svg")
          h2 Rate
          p Upvote reports to improve credibility, and rate your teachers and school administrators.
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
