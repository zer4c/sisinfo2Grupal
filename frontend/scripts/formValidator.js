const validators = {
  code: (value) => {
    if (!value) return "El código de clase es requerido";
    if (value.length < 3) return "El código debe tener al menos 3 caracteres";
    if (value.length > 10) return "El código debe tener máximo 10 caracteres";
    if (!/^[a-zA-Z0-9]+$/.test(value)) return "El código solo puede contener letras y números";
    return null;
  },

  name: (value) => {
    if (!value) return "El nombre de la clase es requerido";
    if (value.length < 3) return "El nombre debe tener al menos 3 caracteres";
    if (value.length > 100) return "El nombre debe tener máximo 100 caracteres";
    return null;
  },

  period: (value) => {
    if (!value) return "La fecha de inicio es requerida";
    const selected = new Date(value);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    if (selected < today) return "La fecha no puede ser en el pasado";
    return null;
  },

  max_students: (value) => {
    if (!value) return "El máximo de estudiantes es requerido";
    if (!/^\d+$/.test(value)) return "Debe ser un número entero";
    const num = Number(value);
    if (num < 1) return "Debe haber al menos 1 estudiante";
    if (num > 200) return "No puede exceder 200 estudiantes";
    return null;
  },

  description: (value) => {
    if (value && value.length > 500) return "La descripción no puede exceder 500 caracteres";
    return null;
  }
};

export function validateForm(data) {
  const errors = {};

  for (const field in validators) {
    const error = validators[field](data[field]);
    if (error) errors[field] = error;
  }

  return errors;
}

