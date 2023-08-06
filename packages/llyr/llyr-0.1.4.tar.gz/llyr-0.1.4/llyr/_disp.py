from typing import Tuple, Union
import multiprocessing as mp

import h5py
import dask.array as da
from tqdm.notebook import tqdm
import numpy as np
import psutil
from dask.distributed import Client


class Disp:
    def __init__(self, h5):
        self.h5 = h5

    def disp(
        self,
        dset: str = "WG",
        name: str = "disp",
        slices: Tuple[Union[int, slice], ...] = (
            slice(None),
            slice(None),
            slice(None),
            slice(None),
            2,
        ),
        save: bool = True,
        force: bool = False,
    ) -> None:
        """Calculates and returns the dispersions using dask"""
        if name in self.h5.dsets():
            if force:
                with h5py.File(self.h5.h5_path, "a") as f:
                    del f[name]
            else:
                input_string: str = input(
                    f"{name} is already a dataset, [y] to overwrite, [n] to cancel, else [input] a new name"
                )
                if input_string.lower() == "y":
                    with h5py.File(self.h5.h5_path, "a") as f:
                        del f[name]
                elif input_string.lower() == "n":
                    return
                else:
                    name = input_string
        dask_client = self.start_dask_client()
        with h5py.File(self.h5.h5_path, "r") as f:
            arr = da.from_array(f[dset], chunks=(None, None, 15, None, None))
            arr = arr[slices]  # slice
            arr = da.multiply(
                arr, np.hanning(arr.shape[0])[:, None, None, None]
            )  # hann filter on the t axis
            arr = arr.sum(axis=1)  # t,z,y,x => t,y,x sum of z
            arr = da.moveaxis(arr, 1, 0)  # t,y,x => y,t,x swap t and y
            ham2d = np.sqrt(
                np.outer(np.hanning(arr.shape[1]), np.hanning(arr.shape[2]))
            )  # shape(t, x)
            arr = da.multiply(arr, ham2d[None, :, :])  # hann window on t and x
            arr = da.fft.fft2(arr)  # 2d fft on t and x
            arr = da.subtract(
                arr, da.average(arr, axis=(1, 2))[:, None, None]
            )  # substract the avr of t,x for a given y
            arr = da.moveaxis(arr, 0, 1)
            arr = arr[: arr.shape[0] // 2]  # split f in 2, take 1st half
            arr = da.fft.fftshift(arr, axes=(1, 2))
            arr = da.absolute(arr)  # from complex to real
            arr = da.sum(arr, axis=1)  # sum y
            out = arr.compute()
        dask_client.close()

        if save:
            with h5py.File(self.h5.h5_path, "a") as f:
                dset_disp = f.create_dataset(name, data=out)
                dset_disp.attrs["slices"] = str(slices)
                dset_disp.attrs["dset"] = dset

    def fft(
        self,
        dset: str = "ND",
        name: str = "fft",
        slices: Tuple[Union[int, slice], ...] = (
            slice(None),
            slice(None),
            slice(None),
            slice(None),
            2,
        ),
        save: bool = True,
    ) -> np.ndarray:
        """Calculates and return the fft of the dataset"""
        with h5py.File(self.h5.h5_path, "a") as f:
            if slices is None:
                arr = f[dset][:]
            else:
                arr = f[dset][slices]
            arr -= arr[0]

            for i in [0, 2, 3]:
                if arr.shape[i] % 2 == 0:
                    arr = np.delete(arr, 1, i)

            hann = np.hanning(arr.shape[0])
            for i, _ in enumerate(hann):
                arr[i] *= hann[i]

            arr = arr.sum(axis=1)  # t,z,y,x,c => t,y,x,c
            fft = []  # fft for each cell and comp
            for y in tqdm(
                range(arr.shape[1]),
                desc="Calculating FFT",
                total=arr.shape[1],
                leave=False,
            ):  # y
                for x in range(arr.shape[2]):  # x
                    for c in range(arr.shape[3]):
                        d = arr[:, y, x, c]
                        d = d - np.average(d)
                        fft.append(np.fft.rfft(d))
            out = np.array(fft)
            out = np.abs(out)
            out = np.sum(out, axis=0)
            out /= (
                arr.shape[1] * arr.shape[2]
            )  # changing the amplitude on a per cell basis

            if save:
                dset_fft = f.create_dataset(name, data=out)
                dset_fft.attrs["slices"] = str(slices)
                dset_fft.attrs["dset"] = dset
        return out

    @property
    def freqs(self) -> np.ndarray:
        """returns frequencies in GHz depending on the number of t points in the dset and value of dt"""
        with h5py.File(self.h5.h5_path, "r") as f:
            freqs = np.fft.rfftfreq(f["disp"].shape[0], self.h5.dt * 1e9)

        return freqs

    @property
    def kvecs(self) -> np.ndarray:
        """returns wavevectors"""
        with h5py.File(self.h5.h5_path, "r") as f:
            kvecs = (
                np.fft.fftshift(
                    np.fft.fftfreq(f["disp"].shape[1], self.h5.dx) * 2 * np.pi
                )
                * 1e-6
            )
        return kvecs

    def start_dask_client(self, port=23232):
        ram = int(psutil.virtual_memory().free / 1e9 * 0.95)
        print(f"Dask client started at 127.0.0.1:{port} with {ram} GB of ram")
        client = Client(
            processes=False,
            threads_per_worker=mp.cpu_count(),
            n_workers=1,
            memory_limit=f"{ram} GB",
        )
        return client
