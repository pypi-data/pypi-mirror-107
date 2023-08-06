from napari_arnheim.widgets.dialogs.upload import createDataArrayFromLayer
from napari_arnheim.dialogs.upload import UploadFileDialog
from grunnlag.schema import Representation, RepresentationVariety, Sample
from bergen.models import Node
from bergen.console import console
from napari_arnheim.context import gui_qt
import argparse
from napari_arnheim.dialogs.upload import UploadFileDialog
from dask_image import ndfilters
from skimage import data
from bergen.console import console
from bergen.models import Node
import xarray as xr


parser = argparse.ArgumentParser()
parser.add_argument('--config', help='Which config file to use', default="bergen.yaml", type=str)
args = parser.parse_args()


def main():
    print(args)

    bergen_params = {
        "config_path": args.config
    }

    with gui_qt(bergen_params=bergen_params) as interface:

        @interface.client.template(Node.objects.get(package="Elements", interface="show"), kabums=False)
        async def show(rep: Representation) -> Representation:
            try:
                interface.helper.openRepresentationAsLayer(rep=rep)
            except:
                console.print_exception()
            return rep

        @interface.client.template(Node.objects.get(package="Elements", interface="gaussian_blur"), kabums=False)
        def gaussian_filter(rep: Representation, sigma: int = 4) -> Representation:
            out = rep.data.data
            filtered = xr.DataArray(out, dims=rep.data.dims)
            return Representation.objects.from_xarray(filtered, name=rep.name + "blured", sample=rep.sample.id, tags=[], variety=RepresentationVariety.VOXEL)


        @interface.client.template(Node.objects.get(package="Elements", interface="upload_active"), test=True)
        async def upload(name: str = None, sample: Sample = None) -> Representation:
            array, name = await interface.widget.createRepresentationFromCurrent(name=name)
            rep = await Representation.asyncs.from_xarray(array, name=name or "test", sample=sample.id if sample else None, tags=[], variety=RepresentationVariety.VOXEL)
            return rep



if __name__ == "__main__":
    main()