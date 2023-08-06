from . import client

import diagmap
import numpy as np

def create_mapping(config, parts, points, phi, n_turns, period = 1, surf_dims = 1, step_size = 1e-3):
    """
    
    Create a mapping from field-lines on given start points.
    
    Args:
        config: Magnetic configuration
        parts: Boundary for tracing
        points: Array-like of shape [3, ...] with at least surf_dims + 1 dimensions. These points indicate starting points for field-line in flux-surfaces.
        phi: 1D Array-like representing the phi cross-sections to calculate in.
        n_turns: Number of tracing turns for every surface & cross-section.
        period: Periodicity for mapping.
        surf_dims: Number of dimensions in the points array (skipping first dimension, as that is the xyz dimension) that identify distinct flux-surfaces. All later dimensions are collapsed after Poincare tracing.
        step_size: Step size to use for tracing
    
    Returns:
        A diagmap.Mapping callable flux surface mapping.
    """
        
    phi = np.asarray(phi)
    assert len(phi.shape) == 1
    
    points = np.asarray(points)
    assert len(points.shape) >= 2
    assert points.shape[0] == 3
    
    n_surf   = np.prod(points.shape[1:1+surf_dims])
    
    if(len(points.shape) > 1 + surf_dims):
        n_points = np.prod(points.shape[1+surf_dims:])
    else:
        n_points = 1
    
    print("Finding axis")
    _, ax = client.find_axis(config)
    
    print("Tracing poincare map")
    pc = client.poincare_in_phi_planes(
        points, 
        phi,
        n_turns,
        config,
        parts,
        step_size = step_size
    )
    
    # Reshape pc array into target format
    # pc.shape = [3, n_phi] + points.shape[1:] + [n_turns]
    pc = np.reshape(pc, [3, len(phi), n_surf, n_points, n_turns])
    # pc.shape = [3, n_phi, n_surf, n_points, n_turns]
    pc = np.transpose(pc, [0, 2, 3, 4, 1])
    # pc.shape = [3, n_surf, n_points, n_turns, n_phi]
    pc = np.reshape(pc, [3, n_surf, n_points * n_turns, len(phi)])
    # pc.shape = [3, n_surf, n_points * n_turns, n_phi]
    
    print("PC shape:", pc.shape)
    print("Ax shape:", ax.shape)
    
    print("Building mapping")
    mapping = diagmap.Mapping(pc, ax, period = period)
    
    return mapping    