(self["webpackChunk_retrolab_lab_extension"] = self["webpackChunk_retrolab_lab_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _retrolab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @retrolab/ui-components */ "webpack/sharing/consume/default/@retrolab/ui-components/@retrolab/ui-components");
/* harmony import */ var _retrolab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_retrolab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/**
 * The command IDs used by the application plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    /**
     * Toggle Top Bar visibility
     */
    CommandIDs.openRetro = 'retrolab:open';
})(CommandIDs || (CommandIDs = {}));
/**
 * A notebook widget extension that adds a retrolab button to the toolbar.
 */
class RetroButton {
    /**
     * Instantiate a new RetroButton.
     * @param commands The command registry.
     */
    constructor(commands) {
        this._commands = commands;
    }
    /**
     * Create a new extension object.
     */
    createNew(panel) {
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
            tooltip: 'Open with RetroLab',
            icon: _retrolab_ui_components__WEBPACK_IMPORTED_MODULE_5__.retroSunIcon,
            onClick: () => {
                this._commands.execute(CommandIDs.openRetro);
            }
        });
        panel.toolbar.insertAfter('cellType', 'retro', button);
        return button;
    }
}
/**
 * A plugin for the checkpoint indicator
 */
const openRetro = {
    id: '@retrolab/lab-extension:open-retro',
    autoStart: true,
    optional: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__.INotebookTracker, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    activate: (app, notebookTracker, palette, menu, labShell) => {
        // TODO: do not activate if already in a IRetroShell?
        if (!notebookTracker || !labShell) {
            // to prevent showing the toolbar button in RetroLab
            return;
        }
        const { commands, docRegistry, shell } = app;
        const baseUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getBaseUrl();
        const isEnabled = () => {
            return (notebookTracker.currentWidget !== null &&
                notebookTracker.currentWidget === shell.currentWidget);
        };
        commands.addCommand(CommandIDs.openRetro, {
            label: 'Open in RetroLab',
            execute: () => {
                const current = notebookTracker.currentWidget;
                if (!current) {
                    return;
                }
                const { context } = current;
                window.open(`${baseUrl}retro/notebooks/${context.path}`);
            },
            isEnabled
        });
        if (palette) {
            palette.addItem({ command: CommandIDs.openRetro, category: 'Other' });
        }
        if (menu) {
            menu.viewMenu.addGroup([{ command: CommandIDs.openRetro }], 1);
        }
        const retroButton = new RetroButton(commands);
        docRegistry.addWidgetExtension('Notebook', retroButton);
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [openRetro];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.b4d6ae3f11fa9024e4f6.js.map