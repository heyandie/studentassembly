<template lang="jade">
section.page__wrapper
  .content__wrapper
    .content__section
      .about__main-logo
        img(src="/static/img/logo.png", height="64")
      article.content__main
        .about__container
          .about__section
            h2 What is Student Assembly?
            p Student Assembly is a tool that aims to reduce quiet and hard corruption in universities. It is a safe anonymous reporting platform for students and an efficient report management platform for school administrations.
          .about__section
            h2 Corruption in Universities
            p
              | Corruption is most commonly defined as&nbsp;
              strong the misuse or abuse of entrusted power for private gain
              |. It has various forms that we can divide into two categories: quiet corruption and hard corruption.&nbsp;
              strong Quiet corruption
              | &nbsp;occurs when power holders fail to perform their jobs properly without suffering any consequences. For example, a professor regularly not attending class or a school administrator often missing required sessions.&nbsp;
              strong Hard corruption
              | &nbsp;occurs when power holders abuse their power and commit illegal acts for private gain. For example, when a professor bribes a student or asks for sexual favors.
            p Corruption occurs in universities because students aren’t empowered to report while schools want to keep their reputation. Student Assembly tackles this double barrier- it provides a safe anonymous reporting platform for students and an efficient report management platform for school administrations.
          .about__section
            h2 Specific University Problems
            p Specifically, Student Assembly aims to tackle the following quiet and hard corruption problems in universities:
            h3 Hard corruption:
            ul
              li Bribery
              li Sexual Harassment and
              li Discrimination
            h3 Quiet corruption:
            ul
              li Environment
              li Curriculum
              li Accessibility
              li Supplies
              li Enrolment Process
              li School Fees
              li Grades
              li Facilities
              li Policies
              li Administration and
              li Teacher Performance
        .about__container
          .about__section
            h2 Our partners
            .about__partner
              .about__partner-logo
                img(src="/static/img/nimc-logo.png", style="background-color:#0b0b0b;padding:9px;")
              h3 Not in my Country
              p Student Assembly is an idea that originates from a non-profit organization called "Not in my country" (NIMC). NIMC operates in Uganda and Kenya, wherein 25% of university students are bribed. It provides university students with a website where they can rate their professors and school admin and report them for corruption.
              a.button.button--small.button--inverted(href="https://uganda.notinmycountry.org") Visit website
      aside.content__secondary
        h3 Our Team
        p Student Assembly is powered by People Power Against Corruption Inc., a Philippine non-profit organization that fights corruption using nonviolent methods.
        a.button.button--small.button--inverted(href="http://peoplepowerph.org") Visit website

section.page__wrapper.page--light
  .content__wrapper
    .content__section
      article.content__main
        h2 FAQs
      aside.content__secondary

</template>

<script>
export default {
  created () {
    console.log(this)
  }
}
</script>
