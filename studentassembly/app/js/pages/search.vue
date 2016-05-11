<template lang="jade">
section.page__wrapper.page--min-height
  .content__wrapper.content--large
    .content__section
      h2 Results for '{{ $route.query.q }}'
      hr
      .content__full
        .content__half
          h3 Reports
          v-report-list(:reports="reports", :loading="loadingReports")
            template(slot="list_empty")
              img.list__empty-icon(src="/static/img/icons/social/ic_sentiment_dissatisfied_48px.svg")
              p.small No reports found. You may be the first one to report on this case!
              a.button.button--small(v-link="{ name: 'file-a-report' }") File a report
        .content__half
          h3 Staff
          v-rating-list(:ratings="ratings", :loading="loadingRatings")
            template(slot="list_empty")
              img.list__empty-icon(src="/static/img/icons/social/ic_sentiment_dissatisfied_48px.svg")
              p.small No staff members found. See the full list on the rate page.
              a.button.button--small(v-link="{ name: 'rate-staff' }") Submit a rating
</template>

<script>
import ReportList from '../components/report-list.vue'
import RatingList from '../components/rating-list.vue'

export default {
  route: {
    data ({ to: { query: { q }}}) {
      this.fetchResults()
    }
  },
  data () {
    return {
      loadingReports: false,
      loadingRatings: false,
      reports: [],
      ratings: [],
      ratingKeys: {
        id: 'staff_id',
        name: 'staff_name',
        rating: 'values'
      }
    }
  },
  methods: {
    fetchResults () {
      let query = encodeURIComponent(this.$route.query.q).replace(/%20/g, "+")

      this.loadingReports = true
      this.loadingRatings = true

      this.$http.get('report?limit=10&q=' + query).then(
        (response) => {
          this.reports = response.data.reports
          this.loadingReports = false
        },
        (response) => {
          console.log('Failed to retrieve reports')
        }
      )

      this.$http.get('staff?limit=10&q=' + query).then(
        (response) => {
          let ratings = response.data

          for (let oldKey in this.ratingKeys) {
            const newKey = this.ratingKeys[oldKey]
            ratings.forEach((rating) => {
              Object.defineProperty(rating, newKey,
                Object.getOwnPropertyDescriptor(rating, oldKey))
              delete rating[oldKey]
            })
          }

          this.ratings = ratings
          this.loadingRatings = false
        },
        (response) => {
          console.log('Failed to retrieve staff')
        }
      )
    }
  },
  components: {
    'v-report-list': ReportList,
    'v-rating-list': RatingList
  }
}
</script>
