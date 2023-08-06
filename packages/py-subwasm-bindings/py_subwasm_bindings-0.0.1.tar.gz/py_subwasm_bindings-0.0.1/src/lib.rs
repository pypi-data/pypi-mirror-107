// Python Subwasm Bindings
//
// Copyright 2018-2021 Stichting Polkascan (Polkascan Foundation).
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

//! Python bindings for the subwasm utility.
//!
//! py-subwwasm-bindings provides bindings to
//! [subwasm](https://gitlab.com/chevdor/subwasm) utility

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use wasm_testbed::WasmTestBed;
use wasm_loader::Source;
use std::str::FromStr;


/// Retrieves metadata from given source string.
///
/// # Arguments
///
/// * `source_str` - Either local WASM file or URL to Substrate RPC
/// * `message` - The binary message to sign.
///
/// # Returns
///
/// Metadata as JSON string
///
/// # Raises
///
/// * `ValueError` - If source or WASM is invalid
#[pyfunction]
#[text_signature = "(source_str, /)"]
pub fn get_metadata(source_str: String) -> PyResult<String> {
    let source = match Source::from_str(&source_str) {
        Ok(source) => source,
        Err(err) => return Err(PyValueError::new_err(format!("Source error: {}", err.to_string()))),
    };

    let runtime = match WasmTestBed::new(&source) {
        Ok(runtime) => runtime,
        Err(err) => return Err(PyValueError::new_err(format!("WASM error: {}", err.to_string()))),
    };

    return Ok(serde_json::to_string_pretty(runtime.metadata()).unwrap());
}

/// This module is a python module implemented in Rust.
#[pymodule]
fn subwasm(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(get_metadata))?;

    Ok(())
}
