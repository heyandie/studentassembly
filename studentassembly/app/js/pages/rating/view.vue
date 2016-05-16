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
            .button__group.u-fl-r
              v-share-button(type="rate", :type-id="member.id")
            h2.u-mg-b-24
              span {{ member.name }}
              br
              span.header--light {{ member.school }}
            h4.u-mg-b-12 Average of {{ member.votes }} {{ member.votes | pluralize 'rating' }}
            ul.stats
              li.stat(v-for="val in member.rating | orderObjectKeys")
                p.stat__header {{ $key | toTitleCase '_' }}
                span.stat__value {{ val }} / 5

          .form__wrapper
            template(v-if="member.user_rating")
              h3.u-mg-b-24 Your rating
              ul.stats.u-mg-b-24
                li.stat.stat--small(v-for="val in member.user_rating.values | orderObjectKeys")
                  p.stat__header {{ $key | toTitleCase '_' }}
                  span.stat__value {{ val }} / 5
              template(v-if="member.user_rating.comment")
                p {{{ member.user_rating.comment | nl2br }}}
              a.button.button--tiny(@click.prevent="showRatingModal = true") Edit rating
            template(v-else)
              .u-ta-c
                template(v-if="userID !== null")
                  p You have not rated {{ member.name }}.
                  a.button.button--small(@click.prevent="showRatingModal = true") Add rating
                template(v-else)
                  p Log in to rate {{ member.name }}.
                  a.button.button--small(v-link="{ name: 'login' }") Go to Login

          template(v-if="member.ratings.length")
            .form__wrapper(v-for="otherRating in member.ratings")
              h4.u-mg-b-24
                v-avatar(:alias="otherRating.alias", :inline="true", height="28px", width="28px")
                span.u-mg-l-4 {{ otherRating.alias }}'s rating
              ul.stats.u-mg-b-24
                li.stat.stat--small(v-for="val in otherRating.values | orderObjectKeys")
                  p.stat__header {{ $key | toTitleCase '_' }}
                  span.stat__value {{ val }} / 5
              template(v-if="otherRating.comment")
                p {{{ otherRating.comment | nl2br }}}

      aside.content__secondary.content--additional-info
        h4 Related staff members
        .u-mg-t-24(v-for="relatedMember in relatedMembers", v-if="relatedMember.id !== member.id")
          a(v-link="{ name: 'rate-view', params: { 'id': relatedMember.id } }")
            h5 {{ relatedMember.name }}
            p.small
              span {{ relatedMember.school | truncate 36 }}
              br
              strong {{ relatedMember.votes || 'No' }} {{ relatedMember.votes | pluralize 'rating' }}
              span(v-if="relatedMember.votes") &nbsp;&mdash; overall: {{ relatedMember.rating.overall }}

  v-modal(:show.sync="showRatingModal")
    div(slot="content", style="width:300px;")
      i.modal-close.icon.ion-android-close(@click="showRatingModal = false")
      template(v-if="!$loadingRouteData")
        form(@submit.prevent="submitRating")
          .form__element(v-for="(key, val) in member.rating")
            .form__label.u-mg-b-4 {{ key | toTitleCase '_' }}
            .form__radio.u-mg-b-0
              .u-cf
                .u-fl-l
                  input(
                    v-for="i in 5",
                    type="radio",
                    name="{{ key }}_{{ i + 1 }}",
                    data-tooltip="Give {{ i + 1 }} points",
                    value="{{ i + 1 }}",
                    :checked="checkRating(key, i + 1)",
                    @click="updateRating(key, $event)"
                  )
                .u-fl-r
                  small.light {{ rating.values[key] }} / 5
          .form__element
            .form__label Comment
            textarea(
              rows="2",
              name="text",
              placeholder="Write additional comments about {{ member.name }}.",
              v-model="rating.comment"
            )
          .form__element
            button(type="submit") Submit rating

</template>

<script>
import Modal from '../../components/modal.vue'
import Avatar from '../../components/avatar.vue'
import Spinner from '../../components/spinner.vue'
import ShareButton from '../../components/share-button.vue'

function defaultRating () {
  return {
    staff_id: null,
    values: {
      accessibility: 0,
      attendance: 0,
      communication_skills: 0,
      efficiency: 0,
      fairness: 0,
      overall: 0
    },
    comment: ''
  }
}

export default {
  vuex: {
    getters: {
      userID: ({ user }) => user.id
    }
  },
  route: {
    data (transition) {
      return this.$http.get('staff/' + this.$route.params.id).then(
        (response) => ({ member: response.data }),
        (response) => {
          console.log('Failed to retrieve staff member.')
        }
      )
    }
  },
  data () {
    return {
      member: null,
      relatedMembers: [],
      showRatingModal: false,
      rating: defaultRating()
    }
  },
  watch: {
    'member': function (val) {
      this.rating = defaultRating()
      this.rating.staff_id = this.member.id

      if (val.user_rating) {
        Object.keys(this.rating).forEach((key) => {
          this.rating[key] = this.member.user_rating[key]
        })
      }

      this.getOtherStaffMembers()
    }
  },
  methods: {
    checkRating (key, val) {
      return val <= this.rating.values[key]
    },
    updateRating (key, e) {
      this.rating.values[key] = parseInt(e.target.value)
    },
    submitRating () {
      let method = this.member.user_rating ? 'put' : 'post',
          query = this.member.user_rating ? '/' + this.member.user_rating.id : ''

      this.$http('rating' + query, { method: method, data: { rating: this.rating }}).then(
        (response) => {
          this.member.user_rating = response.data
          this.showRatingModal = false
        },
        (response) => {
          console.log('Error', response)
        }
      )
    },
    getOtherStaffMembers () {
      this.$http.get('staff?school=' + this.member.school_id + '&limit=5').then(
        (response) => {
          this.relatedMembers = response.data
        },
        (response) => {
          console.log('Failed to retrieve related members.')
        }
      )
    }
  },
  components: {
    'v-modal': Modal,
    'v-avatar': Avatar,
    'v-spinner': Spinner,
    'v-share-button': ShareButton
  }
}
</script>
