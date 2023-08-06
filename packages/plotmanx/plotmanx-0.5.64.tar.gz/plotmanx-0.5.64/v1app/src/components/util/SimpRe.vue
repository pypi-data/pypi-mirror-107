<template id="modal-template" type="text/x-template">
  <transition name="modal">
    <div :class="window_mask" class="modal-mask">
      <div class="modal-wrapper">
        <div :class="window_background_class" class="modal-table-wrapper">
          <div class="window_top flex-column-content"></div>
          <div class="flex-column-content">
            <div class="window_body">
            </div>
          </div>
          <div class="window_bottom flex-column-content"></div>
          <div class="window_footer flex-column-content">
            <slot name="window_footer">
            </slot>
          </div>
        </div>
        <div :class="window_background_class" class="modal-container">
          <div class="modal-header">
            <slot name="header">
              default header
            </slot>
          </div>
          <div class="modal-body">
            <slot name="body">
              default body
            </slot>
          </div>
          <div class="modal-footer">
            <slot name="footer">

            </slot>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>
<script>
export default {
  name: "SimpRe",
  // eslint-disable-next-line vue/require-prop-types
  props: ["window_background_class", "window_mask"]
}
</script>
<style scoped lang="scss">

  .modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, .5);
    display: table;
    transition: opacity .3s ease;
  }

  .modal-table-wrapper {
    position: absolute;
    display: table-cell;
    vertical-align: middle;
  }

  .modal-wrapper {
    display: table-cell;
    vertical-align: middle;
  }

  .modal-container {
    width: 450px;
    margin: 0px auto;
    transition: all .3s ease;
    font-family: Helvetica, Arial, sans-serif;
  }

  @media (max-width: 414px) {
    .modal-container {
      width: 414px;
    }
  }

  @media (max-width: 360px) {
    .modal-container {
      width: 360px;
    }
  }

  @media (device-width: 375px) {
    .modal-container {
      width: 375px;
    }
  }

  @media (max-width: 320px) {
    .modal-container {
      width: 320px;
    }
  }

  .default {
    padding: 20px 30px;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
  }

  .modal-header h3 {
    margin-top: 0;
    color: #42b983;
  }

  .modal-body {
    margin: 5px 0;
  }

  .modal-default-button {
    float: right;
  }

  .modal-enter {
    opacity: 0;
  }

  .modal-leave-active {
    opacity: 0;
  }

  .modal-enter .modal-container,
  .modal-leave-active .modal-container {
    -webkit-transform: scale(1.1);
    transform: scale(1.1);
  }

  .modal-footer {
    display: flex;
    button {
      border-width: 0px;
      border-style: solid;
      font-size: 10px;
      padding: 10px;
    }
  }

  .bbg_waiting_window {
    &.modal-table-wrapper {
      display: none !important;
    }
    //warningwindow
    background: url('~assets/img/windows/note.png');
    background-size: contain;
    background-repeat: no-repeat !important;

    &:after {
      content: "";
    }
    .modal-body {
      text-align: center;
      position: relative;
    }
    .modal-header {
      font-family: "Playstation3";
      text-align: center;
      bottom: 40px;
      position: relative;
    }
    .modal-footer {
      position: relative;
      > div {
        display: flex;
        flex-wrap: nowrap;
        position: absolute;
        .qbtnswitch {
          background: -webkit-gradient(linear, left top, left bottom, from(#2c3b51), to(#325c64));
          background: linear-gradient(to bottom, #2c3b51 0%, #325c64 100%);
          color: #a3ebf8 !important;
          border-color: #4e6385;
          height: 20px;
          line-height: 20px;
        }
      }
    }
  }

  .std_window_mask {
    background-color: rgba(0, 0, 0, 0.79) !important;
  }
</style>
