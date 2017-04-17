/**
 * @license
 * Visual Blocks Language
 *
 * Copyright 2012 Google Inc.
 * https://developers.google.com/blockly/
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

'use strict';

goog.provide('Blockly.tuby.variables');

goog.require('Blockly.tuby');


Blockly.tuby['declare_var'] = function(block) {
  var argument0 = Blockly.tuby.valueToCode(block, 'variables',
      Blockly.tuby.ORDER_ASSIGNMENT) || 'NULL';
  var dropdown_vartype = block.getFieldValue('varType');
  var text_name = block.getFieldValue('NAME');
  var value_variables = Blockly.tuby.valueToCode(block, 'variables', Blockly.tuby.ORDER_ATOMIC);
  // TODO: Assemble tuby into code variable.
  var code = dropdown_vartype + ' ' + text_name  + ';\n';
  return code;
};

Blockly.tuby['use_var'] = function(block) {
  var text_var = block.getFieldValue('var');
  // TODO: Assemble tuby into code variable.
  var code = text_var;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.tuby.ORDER_NONE];
};



Blockly.tuby['assign_var'] = function(block) {
  var argument0 = Blockly.tuby.valueToCode(block, 'assign',
      Blockly.tuby.ORDER_ASSIGNMENT) || 'NULL';
  var text_var = block.getFieldValue('var');
  var value_assign = Blockly.tuby.valueToCode(block, 'assign', Blockly.tuby.ORDER_ATOMIC);
  // TODO: Assemble tuby into code variable.
  var code = text_var + ' = ' + argument0 + ';\n';
  return code;
};


Blockly.tuby['varis_item'] = function(block) {
  var text_item = block.getFieldValue('item');

  // TODO: Assemble tuby into code variable.
  var code = text_item;
  return code;
};

Blockly.tuby['var_dec'] = function(block) {
  var dropdown_opcion = block.getFieldValue('opcion');
  var text_variable = block.getFieldValue('variable');
  // TODO: Assemble JavaScript into code variable.
  var code = dropdown_opcion +' '+ text_variable +';\n';
  return code;
};