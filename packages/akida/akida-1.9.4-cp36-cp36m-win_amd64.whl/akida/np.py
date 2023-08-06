def np_info_repr(self):
    data = "<akida.np.Info>"
    data += ", ident=" + self.ident.__repr__()
    data += ", types=" + self.types.__repr__()
    return data


def np_mesh_repr(self):
    data = "<akida.np.Mesh>"
    data += ", dma_event=" + self.dma_event.__repr__()
    data += ", dma_conf=" + self.dma_conf.__repr__()
    data += ", nps=" + self.nps.__repr__()
    return data
