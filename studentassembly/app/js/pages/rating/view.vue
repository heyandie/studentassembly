<template lang="jade">
section.page__wrapper.page--min-height
  .content__wrapper
    .content__section
      article.content__main
        .form__wrapper(v-if="$loadingRouteData")
          .spinner__wrapper
            v-spinner
            h4 Loading staff member...
        template(v-if="!$loadingRouteData")
          .form__wrapper
            h2
              span {{ staffMember.name }}
              br
              span.header--light {{ staffMember.school }}
            hr
            h4(v-for="(key, val) in staffMember.rating")
              span {{ toTitleCase(key, "_") }}
              br
              span.header--light {{ val }} / 5
            h4
              span Overall
              br
              span.header--light {{ staffMember.overall_rating }} / 5
            hr
            .button__group
              .pull-right
                a.button.button--small.button--facebook(href="#0")
                  img.button__icon(src="/static/img/fb-logo-white.png", height="14")
                  span Share
                a.button.button--small.button--twitter(target="_blank", href="https://twitter.com/intent/tweet?text=Share%20Report")
                  img.button__icon(src="/static/img/twitter-logo-white.png", height="14")
                  span Tweet
          //- .form__wrapper
          //-   pre {{ staffMember | json 2 }}

      aside.content__secondary
        template(v-if="!$loadingRouteData")
          h3 Your rating
          template(v-if="staffMember.user_rating")
            .u-cf(v-for="(key, val) in staffMember.user_rating.values")
              p.small.pull-left
                strong {{ toTitleCase(key, "_") }}
              p.small.pull-right {{ val }} / 5
            p(v-if="staffMember.user_rating.comment") {{ staffMember.user_rating.comment }}
          template(v-if="!staffMember.user_rating")
            p.small You have not rated {{ staffMember.name }}.
          a.button.button--block.button--small(@click.prevent="showRatingModal = true") {{ staffMember.user_rating ? 'Edit' : 'Add' }} your rating

v-modal(:show.sync="showRatingModal")
  div(slot="content", style="width:300px;")
    i.modal-close.icon.ion-android-close(@click="showRatingModal = false")
    template(v-if="!$loadingRouteData")
      form(@submit.prevent="submitRating")
        .form__element(v-for="(key, val) in staffMember.rating")
          .form__label.u-mg-b-4 {{ toTitleCase(key, "_") }}
          .form__radio.u-mg-b-0
            .u-cf
              .pull-left
                input(
                  v-for="i in 5",
                  type="radio",
                  name="{{ key }}_{{ i + 1 }}",
                  data-tooltip="Give {{ i + 1 }} points",
                  value="{{ i + 1 }}",
                  :checked="checkRating(key, i + 1)",
                  @click="updateRating(key, $event)"
                )
              .pull-right
                small.light {{ rating.values[key] }} / 5
        .form__element
          .form__label.u-mg-b-4 Overall Rating
          .form__radio.u-mg-b-0
            .u-cf
              .pull-left
                input(
                  v-for="i in 5",
                  type="radio",
                  name="overall_{{ i + 1 }}",
                  data-tooltip="Give {{ i + 1 }} points",
                  value="{{ i + 1 }}",
                  :checked="checkRating('overall_rating', i + 1)",
                  @click="updateRating('overall_rating', $event)"
                )
              .pull-right
                small.light {{ rating.overall_rating }} / 5
        .form__element
          .form__label Comment
          textarea(rows="2", name="text", placeholder="Write additional comments about {{ staffMember.name }}.", v-model="rating.comment")
        .form__element
          button(type="submit") Submit rating

</template>

<script>
import Modal from '../../components/modal.vue'
import Spinner from '../../components/spinner.vue'
import { toTitleCase } from '../../util'

export default {
  route: {
    data (transition) {
      return this.$http.get('staff/' + this.$route.params.id).then(
        (response) => ({ staffMember: response.data }),
        (response) => {
          console.log('Failed to retrieve staff member.')
        }
      )
    }
  },
  data () {
    return {
      staffMember: null,
      showRatingModal: false,
      rating: {
        staff_id: null,
        overall_rating: 0,
        values: {
          accessibility: 0,
          attendance: 0,
          communication_skills: 0,
          efficiency: 0,
          fairness: 0
        },
        comment: ''
      }
    }
  },
  methods: {
    toTitleCase: toTitleCase,
    checkRating (key, val) {
      if (key === 'overall_rating')
        return val <= this.rating.overall_rating
      else
        return val <= this.rating.values[key]
    },
    updateRating (key, e) {
      if (key === 'overall_rating')
        this.rating.overall_rating = parseInt(e.target.value)
      else
        this.rating.values[key] = parseInt(e.target.value)
    },
    submitRating () {
      let method = this.staffMember.user_rating ? 'patch' : 'post',
          query = this.staffMember.user_rating ? '/' + this.staffMember.user_rating.id : ''

      this.rating.staff_id = this.staffMember.id
      this.$http('rating' + query, { method: method, data: { rating: this.rating }}).then(
        (response) => {
          this.staffMember.user_rating = response.data
          this.showRatingModal = false
        },
        (response) => {
          console.log('Error', response)
        }
      )
    }
  },
  components: {
    'v-modal': Modal,
    'v-spinner': Spinner
  }
}
</script>
