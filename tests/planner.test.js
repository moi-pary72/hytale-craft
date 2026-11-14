const {test}=require('node:test');const assert=require('node:assert/strict');const {compute}=require('../web/planner.js');
const recipe=(yieldCount,ingredients)=>({yield:yieldCount,ingredients});
test('batch yield, shared surplus and inventory',()=>{const db={A:recipe(1,{B:1,C:1}),B:recipe(2,{Raw:3}),C:recipe(1,{B:1})};let r=compute(db,{A:2},{Raw:1});assert.deepEqual({...r.totals},{Raw:5});assert.equal(r.steps.B,2);assert.equal(r.stock.B,0)});
test('inventory satisfies target without crafting',()=>{const r=compute({A:recipe(1,{Raw:5})},{A:2},{A:2});assert.deepEqual({...r.totals},{});assert.deepEqual({...r.steps},{})});
test('surplus cannot hide self cycle',()=>assert.throws(()=>compute({A:recipe(2,{A:1})},{A:1}),/cycle/));
test('indirect cycle and overflow rejected',()=>{assert.throws(()=>compute({A:recipe(1,{B:1}),B:recipe(1,{A:1})},{A:1}),/cycle/);assert.throws(()=>compute({A:recipe(1,{Raw:999999})},{A:1e12}),/quantity/i)});
test('prototype names are opaque safe keys',()=>{const r=compute({}, {constructor:2});assert.equal(r.totals.constructor,2)});
