<template>
  <div class="container_scroll">
    <div class="row">
      <div class="col col-12-of-12 center">How To Play</div>
    </div>
    <div class="row blockhash">
      <div class="col col-12-of-12 smallsize">
        <p>
          1. Interval: 1-15ETH, the amount of shares must be an integer.
          2. The principal is thawed after 5 days of the share-holding period. No dividends are calculated after
          thawing. Node rewards are normally calculated and can be withdrawn at any time. Node rewards are not
          calculated after withdrawal.
          3. Membership level is V1, V2, V3, 1-5 ETH is V1, 6-10 ETH is V2, 11-15 ETH is V3.
          4. Income from equity: daily dividend of V1 is 0.5%, daily dividend of V2 is 0.7%, and daily dividend of V3
          is
          1%.
          5. Node reward: V1: only get the first generation reward, 50% of the daily dividend of the first generation,
          V2: only get the second generation reward, 70% of the daily dividend of the first generation, 50% of the
          daily
          dividend of the second generation, V3: get the unlimited generation reward, 100% of the daily dividend of
          the
          first generation, 70% of the daily dividend of the second generation, 50% of the daily dividend of the third
          generation, 10% of the daily dividend of the fourth generation to the tenth generation, 5% of the daily
          dividend of the 11-20 generation and more than 1% of the daily dividend.
          6. Reward burns: When the amount of his account is less than that of the recommended member, the node reward
          is calculated on the basis of the amount of his account. When the amount of his account is greater than or
          equal to that of the recommended member, the node reward is calculated on the basis of the amount of the
          recommended member. In addition, node rewards need to be multiplied by membership grade coefficient, V1 is
          30%, V2 is 60%, V3 is 100%. For example: A recommended B, A shares 5ETH, B shares 15ETH, then A gets a daily
          bonus of (5*1/100)*50%*30%.
          7. 4% of the share will be automatically allocated to a special account, 2% of which will be used for
          ecological application development and construction, 1% for market development, 1% for incentives for
          founding
          teams, and 70% of the monthly income will be used to counter-supplement the dividend-sharing game.
          8. Dividends and nodal incentives are issued automatically, if the amount is greater than or equal to 0.1,
          it
          will be issued automatically, otherwise, it will accumulate in the account and be issued automatically after
          the amount is greater than or equal to 0.1.
          9. Restart mechanism: If the contract balance is 0, the restart mechanism will be automatically started.
          When
          restart, all accounts will be returned to 0, but the node relationship remains unchanged, and a new round of
          games will be started.
        </p>
      </div>
    </div>
    <div class="row">
      <div class="col col-12-of-12 center">Where to get coin</div>
    </div>
    <div class="row blockhash">
      <div class="col w-auto smallsize">
        <p> The player can obtain the tokens from the top listed exchange platforms. HOTBIT.io, FCOIN.com, EXX.com,
        and ZBG.com.</p>
      </div>
    </div>
    <div class="row">
      <div class="col col-12-of-12 center">Team</div>
    </div>
    <div class="row blockhash">
      <div class="col col-12-of-12 smallsize">
        <p> Our team is from all over the world. At present, there are 26 people in our team. They are from the United
        States, China, Korea, Japan and the United Kingdom. The initiator of this smart contract game is from
        beautiful Cosmo, USA. We have common hobbies and goals. We firmly believe that the smart contract of block
        chain will bring a fundamental revolution to the Internet. We know each other because of our love for block
        chain technology. We will start with the dividend-sharing game and develop a series of open fair fair-minded
        intelligence contract applications based on block chain technology. Please look forward to it.
        </p>
      </div>
    </div>
    <div class="row">
      <nuxt-link class="bbg_login_back" to="#" @click.native="$emit('back')">
        <small>Return 返回</small>
      </nuxt-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "WfxRules"
}
</script>

<style scoped lang="scss">

  $btn-box-height: 8px;
  $cover_bg_x: rgba(52, 29, 22, 0.86);
  $cover_bg_x2: rgba(0, 75, 123, 0.86);

  .smallsize {
    font-size: 10px;
  }

  .blockhash {
    .col {
      margin: 5px;
    }
    p {
      text-align: left;
    }
  }

  .container_scroll {
    color: #73ff4a;
    overflow-y: auto;
    height: 70vh;
    .session_back_color_deepblue {
      background-color: $cover_bg_x2;
      padding-top: 10px;
      padding-bottom: 90px;
    }
    .control_face_cover {
      background-color: $cover_bg_x;
      padding-top: 10px;
      padding-bottom: 90px;
    }
    .control_inclusive {
      padding-top: 10px;
      padding-bottom: 90px;
      background-color: $cover_bg_x2;

      .pad_area {
        display: flex;
        flex-direction: row;
        flex-wrap: nowrap;
        .section_title {
          width: auto !important;
          font-size: 10px;
          margin-left: 10px;
          display: block;
          background: red;
          line-height: 20px;
          padding: 0;
          align-self: center;
        }
      }
    }
  }

</style>
