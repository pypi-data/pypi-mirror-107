extern crate inflector;
use inflector::Inflector;
use std::process::Command;
use serde_json::Value;

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;


#[pyfunction]
pub fn dpkg_dict(mut str_vec: Vec<String>) -> PyResult<String> {
    //mut str_vec: Vec<String>
    // let mut str_vec = vec!["Status".to_string()];
    str_vec.insert(0, "Package".to_string());
    let orig_str_vec = str_vec.clone();
    for str in str_vec.iter_mut(){
        let mut s = String::from("${");
        s.push_str(str.to_title_case().as_str());
        s.push('}');
        *str = s
    }

    let output = match Command::new("sh")
        .args(&["-c", format!("dpkg-query -Wf '{}\t\n';", str_vec.join("<==>")).as_str()])
        .output(){
        Ok(data) => {String::from_utf8_lossy(&data.stdout).to_string()}
        Err(e) => {format!("ERR {}", e)}
    };

    let mut main: Value = Default::default();
    for i in output.trim_end().split("\t\n"){
        let mut xxx: Value = Default::default();
        let i: Vec<&str> = i.split("<==>").collect();

        for (idx,comm) in orig_str_vec.clone().iter().enumerate(){
            if idx != 0{
                xxx[comm] = Value::from(i[idx])
            }
        }
        main[i[0]] = xxx
    }

    //println!("{}", main)
    Ok(main.to_string())
}


/*#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}*/


#[pymodule]
fn dpkg_json(_py: Python, m: &PyModule) -> PyResult<()> {
    //m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(dpkg_dict, m)?)?;

    Ok(())
}