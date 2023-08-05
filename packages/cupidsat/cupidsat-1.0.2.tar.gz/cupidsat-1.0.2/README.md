# CuPID (Python Library)

This is a library for python used for downloading and working with CuPID data.

Install via pip:
```
pip install cupidsat
```
Import using cupid:
```
import cupid
cupid.xray.plot(trange=['YYYY-MM-DD/HH:MM','YYYY-MM-DD/HH:MM']
```
Detailed documentation can be found for each data product:
* X-Ray Telescope
* Dosimeter
* Magnetometer
* Survey data (Combined Low-Cadence X-Ray, Dosimeter, Magnetometer, and Housekeeping)

For IDL, see the CuPID SPEDAS module.

If you make use of this code, please cite the mission paper:
```
@article{Walsh2021,
  doi = {10.1029/2020ja029015},
  url = {https://doi.org/10.1029/2020ja029015},
  year = {2021},
  month = apr,
  publisher = {American Geophysical Union ({AGU})},
  volume = {126},
  number = {4},
  author = {B. M. Walsh and M. R. Collier and E. Atz and L. Billingsley and J. M. Broll and H. K. Connor and D. Chornay and T. Cragwell and N. Dobson and S. Eckert and D. Einhorn and G. Gallant and K. Jackson and S. Karki and J. Kujawski and K. D. Kuntz and V. Naldoza and R. A. Nutter and J. Moore and C. O'Brien and A. Perez-Rosado and F. S. Porter and D. G. Sibeck and K. Simms and W. Skelton and N. Thomas and D. L. Turner and A. Yousuff and A. Weatherwax and A. Zosuls and E. Thomas},
  title = {The Cusp Plasma Imaging Detector ({CuPID}) {CubeSat} Observatory: Mission Overview},
  journal = {Journal of Geophysical Research: Space Physics}
}
```
