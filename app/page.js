import MaterialForm from '../components/MaterialForm';
import Comparison from '../components/Comparison';

export default function Home() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">EAF Raw Material VIU Comparison Tool</h1>
      <p className="mb-6">Add materials, then compare two with a blend.</p>
      <MaterialForm />
      <Comparison />
    </div>
  );
}
