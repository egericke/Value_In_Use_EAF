import MaterialForm from '../components/MaterialForm';
import ComparisonTable from '../components/ComparisonTable';

export default function Home() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">EAF Raw Material VIU Comparison Tool</h1>
      <MaterialForm />
      <ComparisonTable />
    </div>
  );
}
