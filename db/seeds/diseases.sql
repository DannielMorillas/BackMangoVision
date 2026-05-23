-- Catálogo de enfermedades de Mango Kent (EN-021)
-- Idempotente: ON CONFLICT DO NOTHING permite re-ejecutar sin error.

INSERT INTO diseases (slug, name, color_hex, description) VALUES
    (
        'sano',
        'Fruto sano',
        '#22C55E',
        'Fruto de mango Kent sin signos visibles de enfermedad. Coloración uniforme, sin lesiones ni manchas anómalas.'
    ),
    (
        'antracnosis',
        'Antracnosis',
        '#DC2626',
        'Enfermedad fúngica causada por Colletotrichum gloeosporioides. Manchas oscuras circulares hundidas en la superficie del fruto, con tejido necrótico que se expande en condiciones húmedas.'
    ),
    (
        'oidio',
        'Oídio',
        '#A855F7',
        'Enfermedad fúngica causada por Oidium mangiferae. Polvo blanquecino sobre flores, hojas jóvenes y frutos pequeños, que provoca caída prematura y deformaciones.'
    ),
    (
        'pudricion_peduncular',
        'Pudrición del pedúnculo',
        '#F97316',
        'Pudrición en la zona del pedúnculo causada principalmente por Lasiodiplodia theobromae y Dothiorella sp. Aparece tras la cosecha y reduce la aptitud para exportación.'
    ),
    (
        'otras_lesiones',
        'Otras lesiones',
        '#FACC15',
        'Lesiones de causa diversa: daño mecánico, quemaduras de sol, picaduras de insectos u otras enfermedades no clasificadas explícitamente en este catálogo.'
    )
ON CONFLICT (slug) DO NOTHING;
