/*!
 * Copyright (c) 2012 - 2021, Anaconda, Inc., and Bokeh Contributors
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 * 
 * Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 * 
 * Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 * 
 * Neither the name of Anaconda nor the names of any contributors
 * may be used to endorse or promote products derived from this software
 * without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
 */
(function(root, factory) {
  factory(root["Bokeh"], undefined);
})(this, function(Bokeh, version) {
  var define;
  return (function(modules, entry, aliases, externals) {
    const bokeh = typeof Bokeh !== "undefined" && (version != null ? Bokeh[version] : Bokeh);
    if (bokeh != null) {
      return bokeh.register_plugin(modules, entry, aliases);
    } else {
      throw new Error("Cannot find Bokeh " + version + ". You have to load it prior to loading plugins.");
    }
  })
({
"7e6ecbb3c3": /* index.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const tslib_1 = require("tslib");
    const PanelChemistryExtensions = tslib_1.__importStar(require("6ed169d807") /* ./bokeh_extensions/ */);
    exports.PanelChemistryExtensions = PanelChemistryExtensions;
    const base_1 = require("@bokehjs/base");
    base_1.register_models(PanelChemistryExtensions);
},
"6ed169d807": /* bokeh_extensions\index.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    var jsme_editor_1 = require("935e6c4794") /* ./jsme_editor */;
    __esExport("JSMEEditor", jsme_editor_1.JSMEEditor);
},
"935e6c4794": /* bokeh_extensions\jsme_editor.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    // See https://docs.bokeh.org/en/latest/docs/reference/models/layouts.html
    const html_box_1 = require("@bokehjs/models/layouts/html_box");
    const dom_1 = require("@bokehjs/core/dom");
    function uuidv4() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
    const notSubscribed = "Not Subscribed";
    function readSDFValue(jsmeElement) {
        var data = jsmeElement.getMultiSDFstack();
        var output = "No multirecords SDF was pasted into the editor ";
        if (data.length > 0) {
            output = data.join("$$$$\n") + "$$$$\n";
        }
        return output;
    }
    function setModelValue(model, jsmeElement) {
        console.log("setValue - start", model.value);
        var value = model.value;
        if (model.format === "smiles") {
            console.log("getting smiles");
            value = jsmeElement.smiles();
            console.log("got smiles");
        }
        else if (model.format === "mol") {
            value = jsmeElement.molFile(false);
        }
        else if (model.format === "mol3000") {
            value = jsmeElement.molFile(true);
        }
        else if (model.format === "sdf") {
            value = readSDFValue(jsmeElement);
        }
        else {
            value = jsmeElement.jmeFile();
        }
        if (model.value !== value && value !== null) {
            console.log("setting value", value);
            model.value = value;
        }
        console.log("setValue - end", model.value);
    }
    function setModelValues(model, jsmeElement) {
        console.log("setValues - start");
        setModelValue(model, jsmeElement);
        setOtherModelValues(model, jsmeElement);
        console.log("setValues - end");
    }
    function resetOtherModelValues(model, jsmeElement) {
        if (!model.subscriptions.includes("jme")) {
            model.jme = notSubscribed;
        }
        if (!model.subscriptions.includes("smiles")) {
            model.smiles = notSubscribed;
        }
        if (!model.subscriptions.includes("mol")) {
            model.mol = notSubscribed;
        }
        if (!model.subscriptions.includes("mol3000")) {
            model.mol3000 = notSubscribed;
        }
        if (!model.subscriptions.includes("sdf")) {
            model.sdf = notSubscribed;
        }
        setModelValues(model, jsmeElement);
    }
    function cleanValue(value) {
        if (value === null) {
            return "null";
        }
        else {
            return value;
        }
    }
    function setOtherModelValues(model, jsmeElement) {
        console.log("setOtherValues - start");
        if (model.subscriptions.includes("jme")) {
            model.jme = cleanValue(jsmeElement.jmeFile());
        }
        if (model.subscriptions.includes("smiles")) {
            model.smiles = cleanValue(jsmeElement.smiles());
        }
        if (model.subscriptions.includes("mol")) {
            model.mol = cleanValue(jsmeElement.molFile(false));
        }
        if (model.subscriptions.includes("mol3000")) {
            model.mol3000 = cleanValue(jsmeElement.molFile(true));
        }
        if (model.subscriptions.includes("sdf")) {
            model.sdf = cleanValue(readSDFValue(jsmeElement));
        }
        console.log("setOtherValues - end");
    }
    // The view of the Bokeh extension/ HTML element
    // Here you can define how to render the model as well as react to model changes or View events.
    class JSMEEditorView extends html_box_1.HTMLBoxView {
        constructor() {
            super(...arguments);
            this.JSME = window.JSApplet.JSME;
            this.valueChanging = true;
        }
        connect_signals() {
            super.connect_signals();
            this.connect(this.model.properties.value.change, () => {
                console.log("value change", this.model.value);
                if (!this.valueChanging) {
                    if (this.model.value === "") {
                        this.jsmeElement.reset();
                    }
                    else {
                        this.jsmeElement.readGenericMolecularInput(this.model.value);
                    }
                }
            });
            this.connect(this.model.properties.format.change, () => {
                console.log("format change", this.model.format);
                setModelValue(this.model, this.jsmeElement);
            });
            this.connect(this.model.properties.subscriptions.change, () => {
                console.log("subscriptions change", this.model.subscriptions);
                resetOtherModelValues(this.model, this.jsmeElement);
            });
            this.connect(this.model.properties.options.change, () => {
                console.log("options change", this.model.options);
                this.setJSMEOptions();
            });
        }
        render() {
            console.log("render - start");
            super.render();
            const id = "jsme-" + uuidv4();
            const container = dom_1.div({ class: "jsme-editor", id: id });
            this.el.appendChild(container);
            this.jsmeElement = new this.JSME(id, this.getHeight(), this.getWidth(), {
            // "options": "query,hydrogens,fullScreenIcon",
            });
            this.jsmeElement.readGenericMolecularInput(this.model.value);
            resetOtherModelValues(this.model, this.jsmeElement);
            this.setJSMEOptions();
            const this_ = this;
            // function handleTimeOut(){
            //     this_.valueChanged=false
            //     setModelValues(this_.model, this_.jsmeElement)
            // }
            function showEvent(event) {
                console.log("event", event);
                this_.valueChanging = true;
                setModelValues(this_.model, this_.jsmeElement);
                this_.valueChanging = false;
            }
            this.jsmeElement.setAfterStructureModifiedCallback(showEvent);
            setModelValues(this.model, this.jsmeElement);
            console.log("render - end");
        }
        setJSMEOptions() {
            const options = this.model.options.join(",");
            console.log("options", options);
            this.jsmeElement.options(options);
        }
        getHeight() {
            if ((this.model.sizing_mode === "stretch_height" || this.model.sizing_mode === "stretch_both") && this.el.style.height) {
                return this.el.style.height;
            }
            else if (this.model.height) {
                return this.model.height.toString() + "px";
            }
            else {
                return "100px";
            }
        }
        getWidth() {
            if ((this.model.sizing_mode === "stretch_width" || this.model.sizing_mode === "stretch_both") && this.el.style.width) {
                return this.el.style.width;
            }
            else if (this.model.width) {
                return this.model.width.toString() + "px";
            }
            else {
                return "100px";
            }
        }
        resizeJSMEElement() {
            this.jsmeElement.setSize(this.getWidth(), this.getHeight());
        }
        after_layout() {
            super.after_layout();
            this.resizeJSMEElement();
        }
    }
    exports.JSMEEditorView = JSMEEditorView;
    JSMEEditorView.__name__ = "JSMEEditorView";
    // The Bokeh .ts model corresponding to the Bokeh .py model
    class JSMEEditor extends html_box_1.HTMLBox {
        constructor(attrs) {
            super(attrs);
        }
        static init_JSMEEditor() {
            this.prototype.default_view = JSMEEditorView;
            this.define(({ String, Array }) => ({
                value: [String, ""],
                format: [String, ""],
                options: [Array(String), []],
                jme: [String, ""],
                smiles: [String, ""],
                mol: [String, ""],
                mol3000: [String, ""],
                sdf: [String, ""],
                subscriptions: [Array(String), []],
            }));
        }
    }
    exports.JSMEEditor = JSMEEditor;
    JSMEEditor.__name__ = "JSMEEditor";
    JSMEEditor.__module__ = "panel_chemistry.bokeh_extensions.jsme_editor";
    JSMEEditor.init_JSMEEditor();
},
}, "7e6ecbb3c3", {"index":"7e6ecbb3c3","bokeh_extensions/index":"6ed169d807","bokeh_extensions/jsme_editor":"935e6c4794"}, {});});
//# sourceMappingURL=panel_chemistry.js.map
