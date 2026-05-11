use pyo3::prelude::*;
use std::env;

#[pyfunction]
fn run(args: Vec<String>) -> PyResult<u8> {
    ::garbelour::run_cli(args)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{:#}", e)))
}

#[pyfunction]
fn run_with_argv() -> PyResult<()> {
    // argv[0] is python; skip it so argv[1] (the entry-point script) becomes args[0] for clap
    let args: Vec<String> = env::args().skip(1).collect();
    match ::garbelour::run_cli(args) {
        Ok(0) => Ok(()),
        Ok(code) => {
            std::process::exit(code as i32);
        }
        Err(e) => {
            eprintln!("garbelour: {:#}", e);
            std::process::exit(2);
        }
    }
}

#[pymodule]
fn garbelour(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(run, m)?)?;
    m.add_function(wrap_pyfunction!(run_with_argv, m)?)?;
    Ok(())
}
